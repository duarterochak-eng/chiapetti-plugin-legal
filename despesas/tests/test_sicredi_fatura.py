import sys
import tempfile
import unittest
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import sicredi_fatura as sf  # noqa: E402

# Fixtures 100% sintéticas (valores e identificação inventados). Reproduzem a ESTRUTURA
# observada em faturas reais Sicredi: rótulos do resumo, anuidade/IOF/multa dentro de
# "Brasil", crédito de anuidade em "Pagamentos/Créditos", "Valor em Dólar" vazio e
# "Pagamento Mínimo" no cabeçalho.


def montar(resumo, linhas, minimo="R$ 90,00", total_cab=None):
    q = lambda s: f'"{s}"'
    txt = (
        "﻿ Associado ;FULANO DE TAL;;;;\n"
        " Cooperativa ;0000;;;;\n"
        " Cartão Mastercard Black;;;;;\n"
        " 0000.00XX.XXXX.0000;;;;;\n\n"
        " Data de Vencimento ;20/10/2026;;;;\n"
        f" Valor Total (R$) ;{q(total_cab or resumo['total'])};;;;\n"
        f" Pagamento Mínimo (R$) ;{q(minimo)};;;;\n"
        " Situação ;Fechada;;;;\n\n"
        " Resumo de Despesas ;;;;;\n"
        f" Total da fatura anterior (R$) ;{q(resumo['anterior'])};;;;\n"
        f" (-) Pagamentos / Creditos (R$) ;{q(resumo['pagamentos'])};;;;\n"
        f" (+) Encargos (R$) ;{q(resumo['encargos'])};;;;\n"
        f" (+) Despesas / Debitos no Brasil (R$) ;{q(resumo['brasil'])};;;;\n"
        f" (+) Despesas / Debitos no exterior (R$) ;{q(resumo['exterior'])};;;;\n"
        f" (=) Total desta fatura (R$) ;{q(resumo['total'])};;;;\n\n"
        " Data ; Descrição ; Parcela ; Valor ; Valor em Dólar ; Adicional ; Nome;\n"
    )
    for data, desc, parc, valor, adic in linhas:
        txt += f'{data};{desc};{parc};"{valor}";;{adic};Nome Ficticio\n'
    return txt


def gravar(txt):
    p = Path(tempfile.mkdtemp()) / "f.csv"
    p.write_text(txt, encoding="utf-8")
    return p


# Caso A: encargos do resumo = 0; anuidade/IOF dentro de Brasil; crédito de anuidade em pagamentos.
LINHAS_A = [
    ("07/09/2026", "Taxa De Anuidade", "", "R$ 20,00", ""),
    ("26/08/2026", "IOF Compra Internacional", "", "R$ 1,00", "4917"),
    ("25/08/2026", "ANTHROPIC  CLAUDE SU     ", "", "R$ 40,00", "4917"),
    ("20/08/2026", "Pag Fat Deb Cc", "", "R$ -500,00", ""),
    ("14/08/2026", "Credito Anuidade Cartao", "", "R$ -10,00", ""),
    ("30/08/2026", "SUPERMERCADOS MACHAD", "", "R$ 200,00", ""),
    ("22/08/2026", "SUPERMERCADOS DEL MORO", "", "R$ 100,00", ""),
    ("06/07/2026", "MERCADOLIVRE MERCAD", "(02/03)", "R$ 100,00", "4917"),
    ("26/11/2025", "FOSSIL", "(10/10)", "R$ 50,00", "4917"),
]
RESUMO_A = dict(anterior="R$ 500,00", pagamentos="R$ -510,00", encargos="R$ 0,00",
                brasil="R$ 471,00", exterior="R$ 40,00", total="R$ 501,00")

# Caso B: encargos de R$ 30,00 no resumo que NÃO aparecem nos lançamentos (juros do saldo financiado).
LINHAS_B = [
    ("06/10/2026", "Taxa De Anuidade", "", "R$ 20,00", ""),
    ("06/10/2026", "Juros De Mora - Multa", "", "R$ 2,00", ""),
    ("02/10/2026", "Pag Fat Deb Cc", "", "R$ -100,00", ""),
    ("28/09/2026", "Iof Adicional Sobre Saldo Financiad", "", "R$ 1,50", ""),
    ("27/09/2026", "Multa Por Atraso", "", "R$ 9,00", ""),
    ("25/09/2026", "ANTHROPIC  CLAUDE SU     ", "", "R$ 40,00", "4917"),
    ("19/09/2026", "JIM COM  AVANCCE         ", "", "R$ 130,00", ""),
    ("15/09/2026", "SUPREMA FARMA SORRIS     ", "", "R$ 170,00", ""),
    ("06/09/2026", "ViraCopoPromotora        ", "", "R$ 100,00", ""),
    ("08/09/2026", "LavanderiaRibeiro        ", "", "R$ 50,00", ""),
    ("24/06/2026", "SOL INDUSTRI Cartao", "(04/10)", "R$ 100,00", ""),
]
RESUMO_B = dict(anterior="R$ 501,00", pagamentos="R$ -100,00", encargos="R$ 30,00",
                brasil="R$ 582,50", exterior="R$ 40,00", total="R$ 1.053,50")


def fat(resumo, linhas, **kw):
    return sf.ler_fatura(gravar(montar(resumo, linhas, **kw)))


class Parsing(unittest.TestCase):
    def test_valores(self):
        self.assertEqual(sf.parse_valor("R$ 1.234,56"), D("1234.56"))
        self.assertEqual(sf.parse_valor("R$ -9.014,73"), D("-9014.73"))
        self.assertEqual(sf.parse_valor("-R$ 5,00"), D("-5.00"))
        self.assertIsNone(sf.parse_valor("  "))
        self.assertIsInstance(sf.parse_valor("R$ 1,10"), D)

    def test_parcela_e_data(self):
        self.assertEqual(sf.parse_parcela("(02/03)"), (2, 3))
        self.assertIsNone(sf.parse_parcela(""))
        self.assertEqual(sf.parse_data("07/10/2026").month, 10)

    def test_leitura_bom_espacos_cabecalho_e_resumo(self):
        f = fat(RESUMO_A, LINHAS_A)
        self.assertEqual(len(f.lancamentos), 9)
        self.assertEqual(f.lancamentos[2].descricao, "ANTHROPIC CLAUDE SU")
        self.assertIn("Pagamento Mínimo (R$)", f.cabecalho)       # fica no cabeçalho...
        self.assertNotIn("Pagamento Mínimo (R$)", f.resumo)       # ...e fora do resumo
        self.assertEqual(f.lancamentos[2].tipo, "exterior")
        self.assertEqual(f.lancamentos[0].tipo, "encargo")
        self.assertEqual(f.lancamentos[3].tipo, "pagamento_fatura")
        self.assertEqual(f.lancamentos[4].tipo, "credito")

    def test_sem_tabela_falha(self):
        with self.assertRaises(ValueError):
            sf.ler_fatura(gravar("a;b;\nc;d;\n"))


class CasoA(unittest.TestCase):
    def setUp(self):
        self.a = sf.analisar(fat(RESUMO_A, LINHAS_A))

    def test_concilia_sem_avisos(self):
        self.assertEqual(self.a["avisos"], [])

    def test_minimo_nao_confunde_com_pagamentos(self):
        self.assertEqual(self.a["pagamento_minimo"], D("90.00"))
        self.assertEqual(self.a["saldo_se_minimo"], D("411.00"))

    def test_totais(self):
        # compras = positivos (511) - anuidade (20) - IOF (1)
        self.assertEqual(self.a["total_despesas"], D("490.00"))
        self.assertEqual(self.a["encargos_itemizados"], D("21.00"))
        self.assertEqual(self.a["credito"], D("-10.00"))
        self.assertEqual(self.a["por_categoria"]["Mercado"], D("300.00"))
        self.assertEqual(self.a["por_categoria"]["Compras online"], D("100.00"))

    def test_parcelas(self):
        p = {l.descricao: l for l in self.a["parcelas_em_curso"]}
        self.assertEqual(p["MERCADOLIVRE MERCAD"].saldo_restante, D("100.00"))
        self.assertEqual(p["FOSSIL"].saldo_restante, D("0"))
        self.assertIn("última parcela", sf.relatorio(self.a))

    def test_pagamento_fora_das_despesas(self):
        self.assertNotIn("Pagamento fatura anterior", self.a["por_categoria"])

    def test_profissional_a_confirmar(self):
        self.assertEqual([l.descricao for l in self.a["profissionais_a_confirmar"]], ["ANTHROPIC CLAUDE SU"])


class CasoB(unittest.TestCase):
    def setUp(self):
        self.a = sf.analisar(fat(RESUMO_B, LINHAS_B, minimo="R$ 250,00"))

    def test_encargos_nao_detalhados_viram_aviso_nao_erro(self):
        self.assertEqual(self.a["encargos_nao_detalhados"], D("30.00"))
        self.assertEqual(len(self.a["avisos"]), 1)
        self.assertIn("30,00", self.a["avisos"][0])
        self.assertTrue(sf.relatorio(self.a).startswith("AVISOS"))

    def test_saldo_financiado_se_so_minimo(self):
        self.assertEqual(self.a["saldo_se_minimo"], D("803.50"))

    def test_encargos_itemizados_e_categorias(self):
        self.assertEqual(self.a["encargos_itemizados"], D("32.50"))   # 20 + 2 + 1,5 + 9
        c = self.a["por_categoria"]
        self.assertEqual(c["Saúde"], D("170.00"))
        self.assertEqual(c["Lazer e restaurantes"], D("100.00"))
        self.assertEqual(c["Vestuário e lavanderia"], D("50.00"))
        self.assertEqual(c["A identificar (JIM COM)"], D("130.00"))
        self.assertEqual(c["Assinaturas"], D("40.00"))

    def test_saldo_restante_parcela(self):
        (p,) = self.a["parcelas_em_curso"]
        self.assertEqual(p.saldo_restante, D("600.00"))   # 6 parcelas de 100


class Divergencias(unittest.TestCase):
    def test_brasil_errado_interrompe(self):
        r = dict(RESUMO_B, brasil="R$ 587,50", total="R$ 1.058,50")
        with self.assertRaises(sf.ConciliacaoError):
            sf.analisar(fat(r, LINHAS_B))

    def test_total_do_resumo_errado_interrompe(self):
        with self.assertRaises(sf.ConciliacaoError):
            sf.analisar(fat(dict(RESUMO_A, total="R$ 999,00"), LINHAS_A))

    def test_total_do_cabecalho_difere_interrompe(self):
        with self.assertRaises(sf.ConciliacaoError):
            sf.analisar(fat(RESUMO_A, LINHAS_A, total_cab="R$ 777,00"))

    def test_pagamentos_errados_interrompe(self):
        r = dict(RESUMO_A, pagamentos="R$ -500,00", total="R$ 511,00")
        with self.assertRaises(sf.ConciliacaoError):
            sf.analisar(fat(r, LINHAS_A))

    def test_encargos_itemizados_no_resumo_sem_aviso(self):
        # Convenção alternativa: Brasil sem anuidade/IOF e Encargos = 21 (itemizados nos lançamentos).
        r = dict(RESUMO_A, encargos="R$ 21,00", brasil="R$ 450,00")
        a = sf.analisar(fat(r, LINHAS_A))
        self.assertEqual(a["avisos"], [])
        self.assertEqual(a["encargos_nao_detalhados"], D("0"))

    def test_campo_ausente_interrompe_e_lista_rotulos(self):
        txt = montar(RESUMO_A, LINHAS_A).replace("(+) Encargos (R$)", "(+) Outro (R$)")
        c = sf.conciliar(sf.ler_fatura(gravar(txt)))
        self.assertTrue(c.erros and "encargos" in c.erros[0])


class Privacidade(unittest.TestCase):
    def test_saida_nao_vaza_identificacao(self):
        f = fat(RESUMO_B, LINHAS_B)
        saida = sf.relatorio(sf.analisar(f)) + repr(f)
        for segredo in ("FULANO", "Associado", "Cooperativa", "0000.00XX", "Nome Ficticio"):
            self.assertNotIn(segredo, saida)

    def test_erro_nao_vaza_identificacao(self):
        txt = montar(RESUMO_A, LINHAS_A).replace("(+) Encargos (R$)", "(+) Outro (R$)")
        msg = " ".join(sf.conciliar(sf.ler_fatura(gravar(txt))).erros)
        self.assertNotIn("FULANO", msg)

    def test_mascara(self):
        self.assertNotIn("1234567890", sf.mascarar("conta 1234567890 x"))


if __name__ == "__main__":
    unittest.main()
