"""Leitor de faturas de cartão Sicredi (CSV). Ver regra-faturas-sicredi.md.

Regras duras: Decimal (nunca float), conciliação obrigatória antes da análise,
nenhum dado de identificação (cartão, conta, cooperativa) sai em relatório.
"""
from __future__ import annotations

import csv
import re
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

CENTAVO = Decimal("0.01")

# Palavras-chave (sem acento, minúsculas) para localizar os campos do resumo.
# Rótulos reais ainda não vistos: ajustar aqui após o primeiro CSV real.
CAMPOS_RESUMO = {
    "anterior": ("fatura anterior", "saldo anterior"),
    "pagamentos": ("pagamento", "credito"),
    "encargos": ("encargo",),
    "brasil": ("brasil", "nacional"),
    "exterior": ("exterior", "internacional"),
    "total": ("total",),
}

# Categorias por palavra-chave na descrição (primeira que casar). Editável.
CATEGORIAS = {
    "Mercado": ("supermerc", "mercado", "atacad", "hortifruti"),
    "Combustível": ("posto", "combust", "shell", "ipiranga"),
    "Restaurante/Delivery": ("restaur", "ifood", "lanche", "pizza", "burger", "padaria", "cafe"),
    "Saúde": ("farma", "drog", "clinica", "laborat", "unimed"),
    "Lazer": ("kart", "cinema", "ingresso", "steam", "playstation", "xbox", "nintendo"),
    "Compras online": ("mercadolivre", "mercado livre", "amazon", "shopee", "magalu"),
    "Vestuário/Perfumaria": ("roupa", "calcad", "boticario", "perfum", "renner", "riachuelo"),
    "Assinaturas": ("netflix", "spotify", "google", "apple", "microsoft", "anthropic", "openai"),
    "Transporte": ("uber", "99app", "estacion", "pedagio", "sem parar"),
}
# Indícios de despesa profissional. Sempre apresentados como "a confirmar".
INDICIOS_PROFISSIONAIS = ("oab", "anthropic", "openai", "jusbrasil", "cartorio", "papelaria",
                          "correios", "tribunal", "adobe", "microsoft", "google workspace")

LIMITE_ROTULO = 10


class ConciliacaoError(Exception):
    """Fatura não concilia com o próprio resumo; análise não deve prosseguir."""


def _sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()


def _limpo(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def parse_valor(texto: str) -> Decimal | None:
    """'R$ 1.234,56' / 'R$ -9.014,73' / '-R$ 5,00' -> Decimal; vazio -> None."""
    t = _limpo(texto)
    if not t:
        return None
    negativo = "-" in t
    t = re.sub(r"[^\d,.]", "", t).replace(".", "").replace(",", ".")
    try:
        v = Decimal(t)
    except InvalidOperation:
        raise ValueError(f"valor inválido: {texto!r}")
    return -v if negativo else v


def parse_data(texto: str) -> date:
    return datetime.strptime(_limpo(texto), "%d/%m/%Y").date()


def parse_parcela(texto: str) -> tuple[int, int] | None:
    m = re.fullmatch(r"\(?\s*(\d+)\s*/\s*(\d+)\s*\)?", _limpo(texto))
    return (int(m.group(1)), int(m.group(2))) if m else None


def mascarar(texto: str) -> str:
    """Oculta sequências longas de dígitos (cartão, conta, CPF/CNPJ) em qualquer saída."""
    return re.sub(r"\d{6,}", lambda m: "*" * len(m.group(0)), texto)


@dataclass
class Lancamento:
    data: date
    descricao: str
    parcela: tuple[int, int] | None
    valor: Decimal
    valor_dolar: Decimal | None
    adicional: bool
    tipo: str  # compra | exterior | pagamento_fatura | encargo
    categoria: str = "A classificar"
    profissional: bool = False

    @property
    def saldo_restante(self) -> Decimal:
        if not self.parcela:
            return Decimal("0")
        atual, total = self.parcela
        return (self.valor * (total - atual)).quantize(CENTAVO)


@dataclass
class Fatura:
    resumo: dict[str, str] = field(repr=False)
    metadados: dict[str, str] = field(repr=False)  # identificação: nunca imprimir
    lancamentos: list[Lancamento]

    def __repr__(self) -> str:  # sem identificação
        return f"Fatura(lancamentos={len(self.lancamentos)})"


def _classificar(desc: str, valor: Decimal, valor_dolar: Decimal | None) -> tuple[str, str, bool]:
    d = _sem_acento(desc)
    if d.startswith("pag fat") and valor < 0:
        return "pagamento_fatura", "Pagamento fatura anterior", False
    if any(k in d for k in ("anuidade", "iof")):
        return "encargo", "Encargos e tarifas", False
    tipo = "exterior" if (valor_dolar is not None or "anthropic" in d) else "compra"
    categoria = next((c for c, ks in CATEGORIAS.items() if any(k in d for k in ks)), "A classificar")
    return tipo, categoria, any(k in d for k in INDICIOS_PROFISSIONAIS)


def ler_fatura(caminho: str | Path) -> Fatura:
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        linhas = []
        for row in csv.reader(f, delimiter=";"):
            cells = [_limpo(c) for c in row]
            while cells and not cells[-1]:
                cells.pop()  # remove o ';' sobrando
            linhas.append(cells)

    inicio = next((i for i, c in enumerate(linhas)
                   if c and _sem_acento(c[0]) == "data"
                   and {"descricao", "parcela", "valor"} <= {_sem_acento(x) for x in c}), None)
    if inicio is None:
        raise ValueError("tabela de lançamentos não encontrada (linha 'Data;Descrição;Parcela;Valor')")

    cab = [_sem_acento(x) for x in linhas[inicio]]
    idx = {nome: cab.index(nome) for nome in ("data", "descricao", "parcela", "valor")}
    idx_usd = next((i for i, n in enumerate(cab) if "dolar" in n), None)
    idx_adic = next((i for i, n in enumerate(cab) if n == "adicional"), None)

    def cel(c, i):
        return c[i] if i is not None and i < len(c) else ""

    meta: dict[str, str] = {}
    for c in linhas[:inicio]:
        if len(c) >= 2 and c[0]:
            meta[c[0]] = c[1]

    lanc = []
    for c in linhas[inicio + 1:]:
        if not c or not cel(c, idx["data"]):
            continue
        valor = parse_valor(cel(c, idx["valor"]))
        if valor is None:
            continue
        usd = parse_valor(cel(c, idx_usd))
        desc = _limpo(cel(c, idx["descricao"]))
        tipo, cat, prof = _classificar(desc, valor, usd)
        lanc.append(Lancamento(parse_data(cel(c, idx["data"])), desc, parse_parcela(cel(c, idx["parcela"])),
                               valor, usd, bool(cel(c, idx_adic)), tipo, cat, prof))
    return Fatura(resumo=meta, metadados=meta, lancamentos=lanc)


def _campo(resumo: dict[str, str], chaves: tuple[str, ...], usados: set[str]) -> tuple[str, Decimal] | None:
    for k, v in resumo.items():
        kn = _sem_acento(k)
        if k in usados or not any(p in kn for p in chaves):
            continue
        try:
            val = parse_valor(v)
        except ValueError:
            continue
        if val is not None:
            return k, val
    return None


def conciliar(f: Fatura) -> list[str]:
    """Retorna lista de divergências (vazia = concilia). Campos não localizados contam como divergência."""
    usados: set[str] = set()
    campos: dict[str, Decimal] = {}
    faltando = []
    # 'total' é buscado por último e só em chaves ainda não usadas
    for nome in ("anterior", "pagamentos", "encargos", "brasil", "exterior", "total"):
        achado = _campo(f.resumo, CAMPOS_RESUMO[nome], usados)
        if achado:
            usados.add(achado[0])
            campos[nome] = achado[1]
        else:
            faltando.append(nome)
    if faltando:
        return [f"campos do resumo não localizados: {', '.join(faltando)} "
                f"(rótulos vistos: {', '.join(sorted(mascarar(k) for k in f.resumo))})"]

    div = []
    esperado = sum(campos[n] for n in ("anterior", "pagamentos", "encargos", "brasil", "exterior"))
    if esperado != campos["total"]:
        # tolera resumo que informa pagamentos como magnitude positiva
        alt = campos["anterior"] - abs(campos["pagamentos"]) + campos["encargos"] + campos["brasil"] + campos["exterior"]
        if alt != campos["total"]:
            div.append(f"resumo não fecha: componentes={esperado} total informado={campos['total']} "
                       f"(diferença {campos['total'] - esperado})")

    soma = defaultdict(Decimal)
    for l in f.lancamentos:
        chave = {"pagamento_fatura": "pagamentos", "encargo": "encargos",
                 "compra": "brasil", "exterior": "exterior"}[l.tipo]
        soma[chave] += l.valor
    # crédito de anuidade (negativo) pertence aos encargos; pagamentos comparados em módulo
    for nome in ("pagamentos", "encargos", "brasil", "exterior"):
        lanc_v, res_v = soma[nome], campos[nome]
        ok = abs(lanc_v) == abs(res_v) if nome == "pagamentos" else lanc_v == res_v
        if not ok:
            div.append(f"{nome}: lançamentos={lanc_v} resumo={res_v} (diferença {lanc_v - res_v})")
    return div


def analisar(f: Fatura) -> dict:
    """Só roda após conciliação; levanta ConciliacaoError se divergir."""
    div = conciliar(f)
    if div:
        raise ConciliacaoError("; ".join(div))
    despesas = [l for l in f.lancamentos if l.tipo in ("compra", "exterior")]
    por_cat: dict[str, Decimal] = defaultdict(Decimal)
    for l in despesas:
        por_cat[l.categoria] += l.valor
    encargos = sum((l.valor for l in f.lancamentos if l.tipo == "encargo"), Decimal("0"))
    return {
        "por_categoria": dict(sorted(por_cat.items(), key=lambda kv: kv[1], reverse=True)),
        "encargos": encargos,
        "parcelas_em_curso": [l for l in despesas if l.parcela],
        "profissionais_a_confirmar": [l for l in despesas if l.profissional],
        "total_despesas": sum(por_cat.values(), Decimal("0")),
    }


def _brl(v: Decimal) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def relatorio(a: dict) -> str:
    out = ["Despesas por categoria"]
    for cat, v in a["por_categoria"].items():
        out.append(f"  {cat:<24}{_brl(v):>16}")
    out.append(f"  {'TOTAL DESPESAS':<24}{_brl(a['total_despesas']):>16}")
    out.append(f"  {'Encargos e tarifas':<24}{_brl(a['encargos']):>16}")
    out.append("\nParcelas em curso (atual/total, saldo restante)")
    for l in a["parcelas_em_curso"] or []:
        out.append(f"  {mascarar(l.descricao[:30]):<30} {l.parcela[0]}/{l.parcela[1]}  "
                   f"{_brl(l.valor):>14}  restam {_brl(l.saldo_restante)}")
    if not a["parcelas_em_curso"]:
        out.append("  (nenhuma)")
    out.append("\nPossíveis despesas profissionais (a confirmar)")
    for l in a["profissionais_a_confirmar"] or []:
        out.append(f"  {l.data:%d/%m/%Y}  {mascarar(l.descricao[:30]):<30} {_brl(l.valor):>14}  a confirmar")
    if not a["profissionais_a_confirmar"]:
        out.append("  (nenhum)")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("uso: python3 -I sicredi_fatura.py FATURA.csv", file=sys.stderr)
        return 1
    fat = ler_fatura(argv[1])
    try:
        print(relatorio(analisar(fat)))
    except ConciliacaoError as e:
        print(f"CONCILIAÇÃO FALHOU, análise interrompida: {mascarar(str(e))}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
