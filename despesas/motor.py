"""Motor de despesas: banco local, regras congeladas e unificação extrato + faturas.

Convenção: `valor` guardado = efeito em caixa para você (negativo = saiu/gastou; positivo = entrou).
Tipos: despesa | renda | transferencia | pagamento_cartao. Os dois últimos ficam FORA do cálculo
(Pix para você mesmo e pagamento de fatura não são gasto: o gasto está dentro da fatura).
"""
from __future__ import annotations

import calendar
import hashlib
import json
import re
import sqlite3
from collections import defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path

import categorias
import extrato_sicredi as ex
import sicredi_fatura as sf

ZERO = Decimal("0")
CONFIG_PADRAO = {"meus_documentos": [], "cartoes": [], "limite_pergunta": "100", "base_cartao": "fatura",
                 "esperados": []}
ENCARGOS = "Financeiro › Encargos de cartão"
TIPOS = ("despesa", "renda", "transferencia", "pagamento_cartao")
SCHEMA = """
CREATE TABLE IF NOT EXISTS lancamentos(
  id TEXT PRIMARY KEY, origem TEXT, conta TEXT, data TEXT, descricao TEXT, doc TEXT, valor TEXT,
  sugestao TEXT, chave TEXT, tipo TEXT, categoria TEXT, status TEXT, mes_ref TEXT, nota TEXT);
CREATE TABLE IF NOT EXISTS importacoes(
  hash TEXT PRIMARY KEY, tipo TEXT, conta TEXT, inicio TEXT, fim TEXT, novos INT, duplicados INT);
"""
_PFX = re.compile(r"^(pagamento pix|recebimento pix|devolucao pix|transf entre contas|compra debito master|"
                  r"liquidacao boleto sicredi|liquidacao boleto|debito convenios|pgto|pagto)\s+")
sugerir = categorias.sugerir


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", sf._sem_acento(s).strip())


def chave(descricao: str) -> str:
    """Identificador estável do estabelecimento/pessoa: CPF/CNPJ quando houver, senão o nome limpo."""
    d = norm(descricao)
    m = re.search(r"\b(\d{14}|\d{11})\b", d)
    if m and any(k in d for k in ("pix", "transf", "boleto", "convenios")):
        return m.group(1)
    d = re.sub(r"\b\d{5,}\b", "", _PFX.sub("", d))
    return re.sub(r"\s+", " ", d).strip() or norm(descricao)


def classificar(origem, descricao, valor, sugestao, regras, cfg):
    """-> (tipo, categoria, status). Regras do usuário têm prioridade sobre qualquer heurística."""
    d = norm(descricao)
    direcao = "entrada" if valor > 0 else "saida"
    for r in regras:
        if (norm(r["match"]) in d and r.get("direcao") in (None, direcao)
                and (r.get("valor") is None or abs(valor) == Decimal(r["valor"]))):
            return r["tipo"], r["categoria"], "regra"
    if origem == "extrato":
        if d.startswith("pagto fatura"):
            return "pagamento_cartao", "Pagamento de cartão", "auto"
        if set(re.findall(r"\d{11}", d)) & set(cfg["meus_documentos"]):
            return "transferencia", "Transferência própria", "auto"
    if sugestao:
        return "despesa", sugestao, "auto"
    tipo = "renda" if valor > 0 else "despesa"
    if abs(valor) >= Decimal(str(cfg["limite_pergunta"])):
        return tipo, "A classificar", "pendente"
    return tipo, "A classificar (pequenos)", "pequeno"


def _hash(*partes) -> str:
    return hashlib.sha1("|".join(str(p) for p in partes).encode()).hexdigest()[:16]


class Banco:
    def __init__(self, pasta):
        self.pasta = Path(pasta)
        self.pasta.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.pasta / "despesas.db")
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)
        self.cfg = {**CONFIG_PADRAO, **self._ler("config.json", {})}
        self.regras: list[dict] = self._ler("regras.json", [])

    # -- persistência -----------------------------------------------------------------
    def _ler(self, nome, padrao):
        p = self.pasta / nome
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else padrao

    def _gravar(self, nome, dado):
        (self.pasta / nome).write_text(json.dumps(dado, ensure_ascii=False, indent=2), encoding="utf-8")

    def salvar_config(self):
        self._gravar("config.json", self.cfg)

    # -- importação -------------------------------------------------------------------
    def _inserir(self, itens) -> tuple[int, int]:
        novos = dup = 0
        for it in itens:
            tipo, cat, st = classificar(it["origem"], it["desc"], it["valor"], it["sug"], self.regras, self.cfg)
            cur = self.db.execute(
                "INSERT OR IGNORE INTO lancamentos VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (it["id"], it["origem"], it["conta"], it["data"].isoformat(), it["desc"], it["doc"],
                 str(it["valor"]), it["sug"], chave(it["desc"]), tipo, cat, st, it["mes"], ""))
            novos += cur.rowcount
            dup += 1 - cur.rowcount
        self.db.commit()
        return novos, dup

    def _ja_importado(self, h) -> bool:
        return self.db.execute("SELECT 1 FROM importacoes WHERE hash=?", (h,)).fetchone() is not None

    def _registrar(self, h, tipo, conta, ini, fim, novos, dup):
        self.db.execute("INSERT INTO importacoes VALUES (?,?,?,?,?,?,?)",
                        (h, tipo, conta, ini.isoformat() if ini else None, fim.isoformat() if fim else None, novos, dup))
        self.db.commit()

    def importar_extrato(self, caminho, conta="sicredi-pf") -> dict:
        h = hashlib.sha256(Path(caminho).read_bytes()).hexdigest()
        if self._ja_importado(h):
            return {"ja_importado": True}
        e = ex.ler_extrato(caminho)  # levanta ExtratoError se não conciliar
        itens = [dict(id=_hash(conta, l.data, l.descricao, l.doc, l.valor, l.saldo), origem="extrato", conta=conta,
                      data=l.data, desc=l.descricao, doc=l.doc, valor=l.valor,
                      sug=sugerir(l.descricao) if l.valor < 0 else None, mes=l.data.strftime("%Y-%m"))
                 for l in e.linhas]
        novos, dup = self._inserir(itens)
        self._registrar(h, "extrato", conta, e.inicio, e.fim, novos, dup)
        return {"ja_importado": False, "novos": novos, "duplicados": dup, "inicio": e.inicio, "fim": e.fim,
                "saldo_anterior": e.saldo_anterior, "saldo_final": e.saldo_final}

    def importar_fatura(self, caminho, cartao) -> dict:
        h = hashlib.sha256(Path(caminho).read_bytes()).hexdigest()
        if self._ja_importado(h):
            return {"ja_importado": True}
        f = sf.ler_fatura(caminho)
        a = sf.analisar(f)  # levanta ConciliacaoError se não conciliar
        venc = a["vencimento"]
        if venc is None:
            raise ValueError("vencimento da fatura não encontrado")
        por_compra = self.cfg["base_cartao"] == "compra"
        itens, vistos = [], defaultdict(int)
        for l in f.lancamentos:
            if l.tipo == "pagamento_fatura":
                continue  # o pagamento já aparece no extrato como pagamento_cartao
            doc = f"{l.parcela[0]}/{l.parcela[1]}" if l.parcela else ""
            a_vista = l.parcela is None and l.tipo in ("compra", "exterior")
            sug = ENCARGOS if l.tipo in ("encargo", "credito") else sugerir(l.descricao)
            k = (cartao, venc, l.data, l.descricao, doc, l.valor)
            vistos[k] += 1
            itens.append(dict(id=_hash(*k, vistos[k]), origem=f"fatura:{cartao}", conta=cartao, data=l.data,
                              desc=l.descricao, doc=doc, valor=-l.valor, sug=sug,
                              mes=(l.data if por_compra and a_vista else venc).strftime("%Y-%m")))
        if a["encargos_nao_detalhados"]:
            itens.append(dict(id=_hash(cartao, venc, "nao-detalhado"), origem=f"fatura:{cartao}", conta=cartao,
                              data=venc, desc="Encargos não detalhados (resumo da fatura)", doc="",
                              valor=-a["encargos_nao_detalhados"], sug=ENCARGOS, mes=venc.strftime("%Y-%m")))
        novos, dup = self._inserir(itens)
        self._registrar(h, f"fatura:{cartao}", cartao, venc, venc, novos, dup)
        return {"ja_importado": False, "novos": novos, "duplicados": dup, "vencimento": venc,
                "avisos": a["avisos"], "total_fatura": a["total_fatura"]}

    def lancar(self, data: date, valor: Decimal, categoria: str, descricao: str, tipo="despesa") -> str:
        """Lançamento manual (dinheiro, pagamento por outro banco). `valor` em módulo."""
        if tipo not in TIPOS:
            raise ValueError("tipo deve ser " + ", ".join(TIPOS))
        v = abs(valor) if tipo == "renda" else -abs(valor)
        i = _hash("manual", data, v, descricao, categoria)
        self.db.execute("INSERT OR IGNORE INTO lancamentos VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (i, "manual", "manual", data.isoformat(), descricao, "", str(v), None, chave(descricao),
                         tipo, categoria, "manual", data.strftime("%Y-%m"), ""))
        self.db.commit()
        return i

    # -- aprendizado ------------------------------------------------------------------
    def reaplicar(self) -> int:
        n = 0
        for r in self.db.execute("SELECT * FROM lancamentos WHERE status!='manual'").fetchall():
            novo = classificar(r["origem"], r["descricao"], Decimal(r["valor"]), r["sugestao"], self.regras, self.cfg)
            if novo != (r["tipo"], r["categoria"], r["status"]):
                self.db.execute("UPDATE lancamentos SET tipo=?, categoria=?, status=? WHERE id=?", (*novo, r["id"]))
                n += 1
        self.db.commit()
        return n

    def _achar(self, prefixo):
        rows = self.db.execute("SELECT * FROM lancamentos WHERE id LIKE ?", (prefixo + "%",)).fetchall()
        if len(rows) != 1:
            raise ValueError(f"id '{prefixo}' {'não encontrado' if not rows else 'ambíguo'}")
        return rows[0]

    def explicar(self, prefixo, categoria, tipo="despesa", nota="", so_este=False, valor_exato=False) -> int:
        """Congela a explicação como regra (vale para todos os lançamentos iguais, passados e futuros).
        `valor_exato`: a regra só vale para esse valor (ex.: prestação de R$ 2.509 ao mesmo favorecido)."""
        if tipo not in TIPOS:
            raise ValueError("tipo deve ser " + ", ".join(TIPOS))
        r = self._achar(prefixo)
        if so_este:
            self.db.execute("UPDATE lancamentos SET tipo=?, categoria=?, status='manual', nota=? WHERE id=?",
                            (tipo, categoria, nota, r["id"]))
            self.db.commit()
            return 1
        direcao = "entrada" if Decimal(r["valor"]) > 0 else "saida"
        valor = str(abs(Decimal(r["valor"]))) if valor_exato else None
        self.regras = [x for x in self.regras if (x["match"], x.get("direcao"), x.get("valor")) != (r["chave"], direcao, valor)]
        regra = {"match": r["chave"], "direcao": direcao, "tipo": tipo, "categoria": categoria, "nota": nota}
        if valor:
            regra["valor"] = valor
        self.regras.insert(0, regra)
        self._gravar("regras.json", self.regras)
        return self.reaplicar()

    def pendentes(self):
        return self.db.execute("SELECT * FROM lancamentos WHERE status='pendente' "
                               "ORDER BY ABS(CAST(valor AS REAL)) DESC").fetchall()

    # -- leitura ----------------------------------------------------------------------
    def resumo(self, mes: str) -> dict:
        rows = self.db.execute("SELECT * FROM lancamentos WHERE mes_ref=?", (mes,)).fetchall()
        entrou, gastou = defaultdict(Decimal), defaultdict(Decimal)
        a_confirmar, fora = ZERO, defaultdict(Decimal)
        for r in rows:
            v = Decimal(r["valor"])
            if r["tipo"] == "renda":
                if r["status"] == "pendente":
                    a_confirmar += v
                else:
                    entrou[r["categoria"]] += v
            elif r["tipo"] == "despesa":
                gastou[r["categoria"]] += -v
            else:
                fora[r["tipo"]] += -v
        grupos: dict[str, dict] = {}
        for cat, v in gastou.items():
            g, item = categorias.grupo_item(cat)
            x = grupos.setdefault(g, {"total": ZERO, "itens": {}})
            x["total"] += v
            x["itens"][item] = x["itens"].get(item, ZERO) + v
        grupos = {g: {"total": x["total"], "itens": dict(sorted(x["itens"].items(), key=lambda kv: -kv[1]))}
                  for g, x in sorted(grupos.items(), key=lambda kv: -kv[1]["total"])}

        ano, m = map(int, mes.split("-"))
        primeiro, ultimo = date(ano, m, 1), date(ano, m, calendar.monthrange(ano, m)[1])
        avisos = []
        if not self.db.execute("SELECT 1 FROM importacoes WHERE tipo='extrato' AND inicio<=? AND fim>=?",
                               (primeiro.isoformat(), ultimo.isoformat())).fetchone():
            avisos.append("nenhum extrato cobre o mês inteiro; entradas e saídas podem estar incompletas")
        falta = [c for c in self.cfg["cartoes"] if not self.db.execute(
            "SELECT 1 FROM lancamentos WHERE origem=? AND mes_ref=? LIMIT 1", (f"fatura:{c}", mes)).fetchone()]
        if falta:
            avisos.append("faltam faturas: " + ", ".join(falta) + " (o total gasto está incompleto)")
        for e in self.cfg["esperados"]:
            if not self.db.execute("SELECT 1 FROM lancamentos WHERE mes_ref=? AND categoria=? AND tipo='despesa' LIMIT 1",
                                   (mes, e["categoria"])).fetchone():
                avisos.append(f"esperado e não encontrado: {e['nome']} ({sf._brl(Decimal(e['valor']))})")
        pend = [r for r in rows if r["status"] == "pendente"]
        if pend:
            avisos.append(f"{len(pend)} lançamento(s) a explicar ({sf._brl(sum(abs(Decimal(r['valor'])) for r in pend))})")
        tot_in, tot_out = sum(entrou.values(), ZERO), sum(gastou.values(), ZERO)
        return {"mes": mes, "entrou": tot_in, "entrou_por_cat": dict(sorted(entrou.items(), key=lambda kv: -kv[1])),
                "entradas_a_confirmar": a_confirmar, "gastou": tot_out, "gastou_por_grupo": grupos,
                "fora_do_calculo": dict(fora), "saldo": tot_in - tot_out, "avisos": avisos}

    def acumulado(self, ano: str) -> dict:
        meses = [r[0] for r in self.db.execute(
            "SELECT DISTINCT mes_ref FROM lancamentos WHERE mes_ref LIKE ? ORDER BY mes_ref", (ano + "-%",))]
        linhas, acc, grupos, tin, tout, incompletos = [], ZERO, defaultdict(Decimal), ZERO, ZERO, []
        for m in meses:
            d = self.resumo(m)
            acc += d["saldo"]; tin += d["entrou"]; tout += d["gastou"]
            linhas.append({"mes": m, "entrou": d["entrou"], "gastou": d["gastou"], "saldo": d["saldo"], "acumulado": acc})
            for g, x in d["gastou_por_grupo"].items():
                grupos[g] += x["total"]
            if any(a.startswith("faltam faturas") for a in d["avisos"]):
                incompletos.append(m)
        return {"ano": ano, "meses": linhas, "entrou": tin, "gastou": tout, "saldo": tin - tout,
                "grupos": dict(sorted(grupos.items(), key=lambda kv: -kv[1])), "meses_incompletos": incompletos}

    def recorrencias(self, min_meses=2):
        g = defaultdict(lambda: {"meses": set(), "total": ZERO, "n": 0, "cat": "", "tipo": "", "nome": ""})
        for r in self.db.execute("SELECT * FROM lancamentos WHERE tipo IN ('despesa','renda')"):
            x = g[r["chave"]]
            x["meses"].add(r["mes_ref"]); x["total"] += abs(Decimal(r["valor"])); x["n"] += 1
            x["cat"], x["tipo"], x["nome"] = r["categoria"], r["tipo"], r["descricao"]
        out = [dict(chave=k, **v, media_mes=(v["total"] / len(v["meses"])).quantize(Decimal("0.01")))
               for k, v in g.items() if len(v["meses"]) >= min_meses]
        return sorted(out, key=lambda x: -x["media_mes"])


def texto_resumo(d: dict) -> str:
    brl = sf._brl
    out = [f"== {d['mes']} =="]
    if d["avisos"]:
        out += ["AVISOS"] + [f"  ! {a}" for a in d["avisos"]] + [""]
    out.append(f"ENTROU   {brl(d['entrou']):>16}")
    out += [f"   {c:<34}{brl(v):>14}" for c, v in d["entrou_por_cat"].items()]
    if d["entradas_a_confirmar"]:
        out.append(f"   (a confirmar: {brl(d['entradas_a_confirmar'])})")
    out.append(f"GASTOU   {brl(d['gastou']):>16}")
    for g, x in d["gastou_por_grupo"].items():
        out.append(f"  {g:<35}{brl(x['total']):>14}")
        if list(x["itens"]) != [g]:
            out += [f"      {i:<31}{brl(v):>14}" for i, v in x["itens"].items()]
    out.append(f"SOBROU/FALTOU {brl(d['saldo']):>12}")
    if d["fora_do_calculo"]:
        nomes = {"transferencia": "transferências próprias", "pagamento_cartao": "pagamento de cartão"}
        out.append("Fora do cálculo (não é gasto): " + "; ".join(f"{nomes[t]} {brl(v)}" for t, v in d["fora_do_calculo"].items()))
    return "\n".join(out)


def texto_acumulado(d: dict) -> str:
    brl = sf._brl
    out = [f"== ACUMULADO {d['ano']} ==", f"{'mês':<10}{'entrou':>16}{'gastou':>16}{'sobrou':>16}{'acumulado':>16}"]
    out += [f"{x['mes']:<10}{brl(x['entrou']):>16}{brl(x['gastou']):>16}{brl(x['saldo']):>16}{brl(x['acumulado']):>16}"
            for x in d["meses"]]
    out.append(f"{'TOTAL':<10}{brl(d['entrou']):>16}{brl(d['gastou']):>16}{brl(d['saldo']):>16}")
    if d["meses_incompletos"]:
        out.append("  ! meses com fatura faltando (total incompleto): " + ", ".join(d["meses_incompletos"]))
    out.append("\nGasto acumulado por grupo")
    out += [f"  {g:<35}{brl(v):>14}" for g, v in d["grupos"].items()]
    return "\n".join(out)
