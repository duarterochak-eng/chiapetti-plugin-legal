import sys
import tempfile
import unittest
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import sicredi_fatura as sf  # noqa: E402

# Fatura 100% sintética. Rótulos do resumo são hipotéticos até haver um CSV real.
def fatura_csv(total="R$ 1.310,00", brasil="R$ 1.200,00"):
    return (
        "﻿ Associado ;FULANO DE TAL;\n"
        " Cartão ;1234567890123456;\n"
        " Fatura anterior ;R$ 500,00;\n"
        " Pagamentos e créditos ;R$ -500,00;\n"
        " Encargos ;R$ 10,00;\n"
        f" Despesas no Brasil ;{brasil};\n"
        " Despesas no exterior ;R$ 100,00;\n"
        f" Total desta fatura ;{total};\n"
        ";;\n"
        " Data ; Descrição ;Parcela;Valor;Valor em Dólar;Adicional;Nome;\n"
        "02/10/2026;Pag Fat Deb Cc   ;;R$ -500,00;;;;\n"
        "03/10/2026;SUPERMERCADOS MACHAD  ;;R$ 700,00;;;;\n"
        "04/10/2026;LOJA ROUPA XYZ  ;(02/03);R$ 300,00;;;;\n"
        "05/10/2026;POSTO IPIRANGA  ;;R$ 200,00;;4917;;\n"
        "06/10/2026;ANTHROPIC  ;;R$ 100,00;US$ 20,00;;;\n"
        "06/10/2026;IOF Compra Internacional  ;;R$ 10,00;;;;\n"
        "07/10/2026;Credito Anuidade Cartao  ;;R$ 0,00;;;;\n"
    )


def gravar(txt):
    d = tempfile.mkdtemp()
    p = Path(d) / "f.csv"
    p.write_text(txt, encoding="utf-8")
    return p


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

    def test_leitura_bom_espacos_e_tabela(self):
        f = sf.ler_fatura(gravar(fatura_csv()))
        self.assertEqual(len(f.lancamentos), 7)
        self.assertEqual(f.lancamentos[1].descricao, "SUPERMERCADOS MACHAD")
        tipos = [l.tipo for l in f.lancamentos]
        self.assertEqual(tipos, ["pagamento_fatura", "compra", "compra", "compra",
                                 "exterior", "encargo", "encargo"])
        self.assertTrue(f.lancamentos[3].adicional)
        self.assertEqual(f.lancamentos[2].saldo_restante, D("300.00"))

    def test_sem_tabela_falha(self):
        with self.assertRaises(ValueError):
            sf.ler_fatura(gravar("a;b;\nc;d;\n"))


class Conciliacao(unittest.TestCase):
    def setUp(self):
        # brasil = 700+300+200 = 1200; exterior = 100; encargos = 10; pagamentos = -500
        self.ok = fatura_csv()

    def test_concilia(self):
        f = sf.ler_fatura(gravar(self.ok))
        self.assertEqual(sf.conciliar(f), [])
        a = sf.analisar(f)
        self.assertEqual(a["total_despesas"], D("1300.00"))
        self.assertEqual(a["por_categoria"]["Mercado"], D("700.00"))
        self.assertEqual(len(a["parcelas_em_curso"]), 1)
        self.assertEqual([l.descricao for l in a["profissionais_a_confirmar"]], ["ANTHROPIC"])

    def test_pagamento_fora_das_despesas(self):
        a = sf.analisar(sf.ler_fatura(gravar(self.ok)))
        self.assertNotIn("Pagamento fatura anterior", a["por_categoria"])

    def test_divergencia_interrompe(self):
        ruim = self.ok.replace("R$ 1.200,00", "R$ 1.250,00")
        f = sf.ler_fatura(gravar(ruim))
        self.assertTrue(sf.conciliar(f))
        with self.assertRaises(sf.ConciliacaoError):
            sf.analisar(f)

    def test_total_errado_interrompe(self):
        f = sf.ler_fatura(gravar(self.ok.replace("R$ 1.310,00", "R$ 999,00")))
        with self.assertRaises(sf.ConciliacaoError):
            sf.analisar(f)


class Privacidade(unittest.TestCase):
    def test_saida_nao_vaza_identificacao(self):
        f = sf.ler_fatura(gravar(fatura_csv()))
        saida = sf.relatorio(sf.analisar(f)) + repr(f)
        for segredo in ("1234567890123456", "FULANO", "Associado"):
            self.assertNotIn(segredo, saida)

    def test_mascara(self):
        self.assertNotIn("1234567890", sf.mascarar("conta 1234567890 x"))


if __name__ == "__main__":
    unittest.main()
