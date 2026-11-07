"""Leitor de faturas de cartão Sicredi (CSV). Ver regra-faturas-sicredi.md.

Regras duras: Decimal (nunca float), conciliação obrigatória antes da análise,
nenhum dado de identificação (cartão, conta, cooperativa) sai em relatório.

Convenção do resumo Sicredi (observada em faturas reais):
  * anuidade, IOF, multa e juros de mora aparecem DENTRO de "Débitos no Brasil";
  * crédito de anuidade aparece em "Pagamentos / Créditos";
  * "Encargos" pode trazer valor que NÃO está itemizado nos lançamentos;
  * "Valor em Dólar" vem vazio; o exterior só se distingue pelo estabelecimento;
  * "Pagamento Mínimo" (cabeçalho) não é "Pagamentos / Créditos" (resumo).
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
ZERO = Decimal("0")

# Rótulos do resumo, comparados sem acento e em minúsculas.
RESUMO_REGEX = {
    "anterior": r"fatura anterior",
    "pagamentos": r"pagamentos?\s*(?:/|e)\s*creditos?",
    "encargos": r"\bencargos\b",
    "brasil": r"no brasil",
    "exterior": r"no exterior",
    "total": r"total desta fatura",
}
CABECALHO_REGEX = {
    "total": r"^valor total",
    "minimo": r"pagamento minimo",
    "vencimento": r"vencimento",
}
# "Valor em Dólar" vem vazio nas faturas reais: exterior só por estabelecimento.
EXTERIOR_HINTS = ("anthropic",)

# Primeira categoria que casar vence (a ordem importa). Editável.
CATEGORIAS = {
    "Compras online": ("mercadolivre", "mercado livre", "amazon", "shopee", "magalu", "magazine luiza"),
    "Mercado": ("supermerc", "atacad", "hortifruti", "mercearia"),
    "Veículo": ("baratao", "posto", "combust", "shell", "ipiranga", "lavajato", "lava jato", "lavego"),
    "Saúde": ("farma", "pharmacia", "drog", "drugstore", "clinica", "laborat", "unimed",
              "biomanip", "formula certa"),
    "Lazer e restaurantes": ("viracopo", "vira copo", "la vie", "taboo", "steak", "restaur", "ifood",
                             "lanche", "pizza", "burger", "padaria", "cafe", "acai", "sorvete",
                             "degustare", "convenienc", "kart", "cinema", "ingresso", "steam",
                             "playstation", "xbox", "nintendo"),
    "Assinaturas": ("netflix", "spotify", "google", "apple com", "microsoft", "anthropic", "openai"),
    "Vestuário e lavanderia": ("lavanderia", "roupa", "calcad", "boticario", "perfum", "renner",
                               "riachuelo", "fossil"),
    "Transporte": ("uber", "99app", "estacion", "pedagio", "sem parar"),
    "A identificar (JIM COM)": ("jim com",),
}
# Indícios de despesa profissional. Sempre apresentados como "a confirmar".
INDICIOS_PROFISSIONAIS = ("oab", "anthropic", "openai", "jusbrasil", "cartorio", "papelaria",
                          "correios", "tribunal", "adobe", "microsoft")


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


def _brl(v: Decimal) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@dataclass
class Lancamento:
    data: date
    descricao: str
    parcela: tuple[int, int] | None
    valor: Decimal
    valor_dolar: Decimal | None
    adicional: bool
    tipo: str  # compra | exterior | encargo | pagamento_fatura | credito
    categoria: str = "A classificar"
    profissional: bool = False

    @property
    def saldo_restante(self) -> Decimal:
        if not self.parcela:
            return ZERO
        atual, total = self.parcela
        return (self.valor * (total - atual)).quantize(CENTAVO)


@dataclass
class Fatura:
    cabecalho: dict[str, str] = field(repr=False)  # identificação: nunca imprimir
    resumo: dict[str, str] = field(repr=False)
    lancamentos: list[Lancamento]

    def __repr__(self) -> str:  # sem identificação
        return f"Fatura(lancamentos={len(self.lancamentos)})"


@dataclass
class Conciliacao:
    erros: list[str]
    avisos: list[str]
    campos: dict[str, Decimal]
    encargos_nao_detalhados: Decimal = ZERO


def _classificar(desc: str, valor: Decimal, valor_dolar: Decimal | None) -> tuple[str, str, bool]:
    d = _sem_acento(desc)
    if valor < 0:
        if d.startswith("pag fat"):
            return "pagamento_fatura", "Pagamento fatura anterior", False
        return "credito", "Créditos e estornos", False
    if any(k in d for k in ("anuidade", "iof", "juros", "multa")):
        return "encargo", "Encargos e tarifas", False
    exterior = valor_dolar is not None or any(h in d for h in EXTERIOR_HINTS)
    categoria = next((c for c, ks in CATEGORIAS.items() if any(k in d for k in ks)), "A classificar")
    return ("exterior" if exterior else "compra"), categoria, any(k in d for k in INDICIOS_PROFISSIONAIS)


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

    cabecalho: dict[str, str] = {}
    resumo: dict[str, str] = {}
    em_resumo = False
    for c in linhas[:inicio]:
        if c and _sem_acento(c[0]).startswith("resumo de despesas"):
            em_resumo = True
            continue
        if len(c) >= 2 and c[0]:
            (resumo if em_resumo else cabecalho)[c[0]] = c[1]
    if not resumo:  # sem marcador "Resumo de Despesas": usa tudo
        resumo = dict(cabecalho)

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
    return Fatura(cabecalho=cabecalho, resumo=resumo, lancamentos=lanc)


def _buscar(campos: dict[str, str], regex: str) -> Decimal | None:
    for k, v in campos.items():
        if re.search(regex, _sem_acento(_limpo(k))):
            try:
                val = parse_valor(v)
            except ValueError:
                continue
            if val is not None:
                return val
    return None


def conciliar(f: Fatura) -> Conciliacao:
    """Erros bloqueiam a análise; avisos são exibidos no topo do relatório."""
    campos: dict[str, Decimal] = {}
    faltando = []
    for nome, rx in RESUMO_REGEX.items():
        v = _buscar(f.resumo, rx)
        if v is None:
            faltando.append(nome)
        else:
            campos[nome] = v
    if faltando:
        vistos = ", ".join(sorted(mascarar(k) for k in f.resumo))
        return Conciliacao([f"campos do resumo não localizados: {', '.join(faltando)} "
                            f"(rótulos vistos: {vistos})"], [], campos)

    erros: list[str] = []
    avisos: list[str] = []
    nao_det = ZERO

    esperado = sum(campos[n] for n in ("anterior", "pagamentos", "encargos", "brasil", "exterior"))
    if esperado != campos["total"]:
        erros.append(f"resumo não fecha: componentes={esperado} total informado={campos['total']} "
                     f"(diferença {campos['total'] - esperado})")
    total_cab = _buscar(f.cabecalho, CABECALHO_REGEX["total"])
    if total_cab is not None and total_cab != campos["total"]:
        erros.append(f"valor total do cabeçalho ({total_cab}) difere do total do resumo ({campos['total']})")

    negativos = sum((l.valor for l in f.lancamentos if l.valor < 0), ZERO)
    if negativos != campos["pagamentos"]:
        erros.append(f"pagamentos/créditos: lançamentos={negativos} resumo={campos['pagamentos']} "
                     f"(diferença {negativos - campos['pagamentos']})")

    positivos = sum((l.valor for l in f.lancamentos if l.valor > 0), ZERO)
    base = campos["brasil"] + campos["exterior"]
    if positivos == base:
        if campos["encargos"] != 0:
            nao_det = campos["encargos"]
            avisos.append(f"encargos de {_brl(nao_det)} constam no resumo e NÃO estão detalhados nos "
                          f"lançamentos (é exatamente a diferença entre resumo e lançamentos); "
                          f"peça o detalhamento ao emissor")
    elif positivos != base + campos["encargos"]:
        erros.append(f"débitos: lançamentos={positivos}; resumo Brasil+exterior={base} "
                     f"(ou {base + campos['encargos']} com encargos); diferença {positivos - base}")

    ext = sum((l.valor for l in f.lancamentos if l.tipo == "exterior"), ZERO)
    if ext != campos["exterior"]:
        avisos.append(f"exterior: lançamentos identificados={ext} resumo={campos['exterior']} "
                      f"(a divisão Brasil/exterior é por estabelecimento; ajuste EXTERIOR_HINTS)")
    return Conciliacao(erros, avisos, campos, nao_det)


def analisar(f: Fatura) -> dict:
    """Só roda após conciliação; levanta ConciliacaoError se houver erro."""
    c = conciliar(f)
    if c.erros:
        raise ConciliacaoError("; ".join(c.erros))
    despesas = [l for l in f.lancamentos if l.tipo in ("compra", "exterior")]
    por_cat: dict[str, Decimal] = defaultdict(Decimal)
    for l in despesas:
        por_cat[l.categoria] += l.valor
    try:
        venc = parse_data(next(v for k, v in f.cabecalho.items()
                               if re.search(CABECALHO_REGEX["vencimento"], _sem_acento(k))))
    except (StopIteration, ValueError):
        venc = None
    minimo = _buscar(f.cabecalho, CABECALHO_REGEX["minimo"])
    total = c.campos["total"]
    return {
        "avisos": c.avisos,
        "vencimento": venc,
        "total_fatura": total,
        "pagamento_minimo": minimo,
        "saldo_se_minimo": (total - minimo) if minimo is not None else None,
        "por_categoria": dict(sorted(por_cat.items(), key=lambda kv: kv[1], reverse=True)),
        "total_despesas": sum(por_cat.values(), ZERO),
        "encargos_itemizados": sum((l.valor for l in f.lancamentos if l.tipo == "encargo"), ZERO),
        "credito": sum((l.valor for l in f.lancamentos if l.tipo == "credito"), ZERO),
        "encargos_nao_detalhados": c.encargos_nao_detalhados,
        "parcelas_em_curso": [l for l in despesas if l.parcela],
        "profissionais_a_confirmar": [l for l in despesas if l.profissional],
    }


def relatorio(a: dict) -> str:
    out: list[str] = []
    if a["avisos"]:
        out.append("AVISOS (leia antes dos números)")
        out += [f"  ! {x}" for x in a["avisos"]]
        out.append("")
    cab = []
    if a["vencimento"]:
        cab.append(f"Vencimento {a['vencimento']:%d/%m/%Y}")
    cab.append(f"Total {_brl(a['total_fatura'])}")
    if a["pagamento_minimo"] is not None:
        cab.append(f"Mínimo {_brl(a['pagamento_minimo'])}")
        cab.append(f"Saldo financiado se pagar só o mínimo {_brl(a['saldo_se_minimo'])}")
    out.append("  |  ".join(cab))
    out.append("\nDespesas por categoria")
    for cat, v in a["por_categoria"].items():
        out.append(f"  {cat:<26}{_brl(v):>16}")
    out.append(f"  {'TOTAL DESPESAS':<26}{_brl(a['total_despesas']):>16}")
    out.append("\nEncargos e tarifas")
    out.append(f"  {'Itemizados':<26}{_brl(a['encargos_itemizados']):>16}")
    out.append(f"  {'Não detalhados (resumo)':<26}{_brl(a['encargos_nao_detalhados']):>16}")
    out.append(f"  {'Créditos (ex.: anuidade)':<26}{_brl(a['credito']):>16}")
    out.append("\nParcelas em curso (atual/total, saldo restante)")
    for l in a["parcelas_em_curso"]:
        resto = "última parcela" if l.parcela[0] == l.parcela[1] else f"restam {_brl(l.saldo_restante)}"
        out.append(f"  {mascarar(l.descricao[:30]):<30} {l.parcela[0]}/{l.parcela[1]}  {_brl(l.valor):>14}  {resto}")
    if not a["parcelas_em_curso"]:
        out.append("  (nenhuma)")
    out.append("\nPossíveis despesas profissionais (a confirmar)")
    for l in a["profissionais_a_confirmar"]:
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
