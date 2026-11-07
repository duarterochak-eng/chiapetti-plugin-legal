import sys
import tempfile
import unittest
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import io  # noqa: E402
from contextlib import redirect_stdout  # noqa: E402

import app  # noqa: E402
import extrato_sicredi as ex  # noqa: E402
import motor  # noqa: E402
import sicredi_fatura as sf  # noqa: E402
from test_sicredi_fatura import LINHAS_B, RESUMO_B, montar  # noqa: E402

# Dados 100% fictícios.
EU, SOCIO, DIARISTA, ITAU = "11111111111", "22222222222", "33333333333", "44444444444444"


def br(v):
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-" if v < 0 else "") + s


def extrato_txt(linhas, saldo_ant=D("1000.00"), periodo="01/10/2026 a 31/10/2026", quebrar=None):
    t = (f"Associado: FULANO | Coop. 0000 | Conta 00000-0 | Período {periodo}\n"
         "Data;Descrição;Documento;Valor;Saldo\n" f";SALDO ANTERIOR;;;{br(saldo_ant)}\n")
    saldo = saldo_ant
    for i, (data, desc, doc, v) in enumerate(linhas):
        saldo += D(v)
        mostrado = saldo + (D("1.00") if quebrar == i else 0)
        t += f"{data};{desc};{doc};{br(D(v))};{br(mostrado)}\n"
    return t


OUT = [
    ("02/10/2026", f"TRANSF ENTRE CONTAS {SOCIO} SOCIO TESTE", "SI01", "5000.00"),
    ("03/10/2026", "PAGTO FATURA MASTER", "030", "-1000.00"),
    ("04/10/2026", f"PAGAMENTO PIX {ITAU} ITAU UNIBANCO HOLDI", "PIX_DEB", "-800.00"),
    ("05/10/2026", f"PAGAMENTO PIX {EU} FULANO DE TAL", "PIX_DEB", "-300.00"),
    ("06/10/2026", f"PAGAMENTO PIX {DIARISTA} Diarista Teste", "PIX_DEB", "-400.00"),
    ("07/10/2026", "COMPRA DEBITO MASTER DEL MORO SUPERMERCADOS SORR", "CM01", "-150.00"),
    ("08/10/2026", "PAGAMENTO PIX 55555555555 Fulano Obra", "PIX_DEB", "-609.00"),
    ("09/10/2026", "PAGAMENTO PIX 66666666666 Pessoa Pequena", "PIX_DEB", "-50.00"),
    ("10/10/2026", "CESTA DE RELACIONAMENTO", "", "-32.00"),
    ("11/10/2026", "RECEBIMENTO PIX 77777777777 CLIENTE X", "PIX_CRED", "2000.00"),
]
NOV = [
    ("02/11/2026", f"TRANSF ENTRE CONTAS {SOCIO} SOCIO TESTE", "SI09", "4000.00"),
    ("04/11/2026", f"PAGAMENTO PIX {ITAU} ITAU UNIBANCO HOLDI", "PIX_DEB", "-900.00"),
    ("06/11/2026", f"PAGAMENTO PIX {DIARISTA} Diarista Teste", "PIX_DEB", "-420.00"),
]


def gravar(txt, nome="f.csv"):
    p = Path(tempfile.mkdtemp()) / nome
    p.write_text(txt, encoding="utf-8")
    return p


def banco():
    b = motor.Banco(tempfile.mkdtemp())
    b.cfg["meus_documentos"] = [EU]
    return b


def explicar_por_nome(b, trecho, categoria, tipo="despesa"):
    r = b.db.execute("SELECT id FROM lancamentos WHERE descricao LIKE ?", (f"%{trecho}%",)).fetchone()
    return b.explicar(r["id"], categoria, tipo)


class Extrato(unittest.TestCase):
    def test_le_e_concilia(self):
        e = ex.ler_extrato(gravar(extrato_txt(OUT)))
        self.assertEqual(len(e.linhas), 10)
        self.assertEqual(e.saldo_anterior, D("1000.00"))
        self.assertEqual(e.saldo_final, D("1000") + sum(D(x[3]) for x in OUT))
        self.assertEqual((e.inicio.day, e.fim.day), (1, 31))

    def test_saldo_quebrado_interrompe(self):
        with self.assertRaises(ex.ExtratoError):
            ex.ler_extrato(gravar(extrato_txt(OUT, quebrar=3)))

    def test_nada_importado_se_nao_concilia(self):
        b = banco()
        with self.assertRaises(ex.ExtratoError):
            b.importar_extrato(gravar(extrato_txt(OUT, quebrar=3)))
        self.assertEqual(b.db.execute("SELECT COUNT(*) FROM lancamentos").fetchone()[0], 0)


class Importacao(unittest.TestCase):
    def test_reimportar_e_sobreposicao_nao_duplicam(self):
        b = banco()
        arq = gravar(extrato_txt(OUT))
        self.assertEqual(b.importar_extrato(arq)["novos"], 10)
        self.assertTrue(b.importar_extrato(arq)["ja_importado"])
        # outro arquivo: 5 primeiras linhas repetidas + 1 nova (mesmos saldos correntes)
        extra = OUT[:5] + [("12/10/2026", "COMPRA DEBITO MASTER PADARIA X", "CM02", "-20.00")]
        r = b.importar_extrato(gravar(extrato_txt(extra), "g.csv"))
        self.assertEqual((r["novos"], r["duplicados"]), (1, 5))
        self.assertEqual(b.db.execute("SELECT COUNT(*) FROM lancamentos").fetchone()[0], 11)


class Classificacao(unittest.TestCase):
    def setUp(self):
        self.b = banco()
        self.b.importar_extrato(gravar(extrato_txt(OUT)))
        self.t = {r["descricao"]: r for r in self.b.db.execute("SELECT * FROM lancamentos")}

    def test_automaticos(self):
        self.assertEqual(self.t["PAGTO FATURA MASTER"]["tipo"], "pagamento_cartao")
        pix_eu = next(r for d, r in self.t.items() if EU in d)
        self.assertEqual(pix_eu["tipo"], "transferencia")
        self.assertEqual(self.t["CESTA DE RELACIONAMENTO"]["categoria"], "Tarifas bancárias")
        mercado = next(r for d, r in self.t.items() if "DEL MORO" in d)
        self.assertEqual(mercado["categoria"], "Mercado")

    def test_so_pergunta_o_que_nao_reconhece_acima_do_limite(self):
        perguntas = {r["descricao"] for r in self.b.pendentes()}
        self.assertTrue(any("ITAU" in d for d in perguntas))
        self.assertTrue(any("Fulano Obra" in d for d in perguntas))      # 609
        self.assertTrue(any("CLIENTE X" in d for d in perguntas))        # entrada desconhecida
        self.assertFalse(any("Pessoa Pequena" in d for d in perguntas))  # 50 < limite
        self.assertFalse(any("DEL MORO" in d for d in perguntas))

    def test_explicar_congela_regra_para_proximos_envios(self):
        n = explicar_por_nome(self.b, "ITAU", "Pagamento de cartão", "pagamento_cartao")
        self.assertEqual(n, 1)
        self.b.importar_extrato(gravar(extrato_txt(NOV, saldo_ant=D("1000.00"), periodo="01/11/2026 a 30/11/2026"), "n.csv"))
        itau_nov = self.b.db.execute("SELECT * FROM lancamentos WHERE descricao LIKE '%ITAU%' AND mes_ref='2026-11'").fetchone()
        self.assertEqual((itau_nov["tipo"], itau_nov["status"]), ("pagamento_cartao", "regra"))
        self.assertNotIn("ITAU", " ".join(r["descricao"] for r in self.b.pendentes()))

    def test_so_este_nao_cria_regra(self):
        r = self.b.db.execute("SELECT id FROM lancamentos WHERE descricao LIKE '%Fulano Obra%'").fetchone()
        self.b.explicar(r["id"], "Presente", so_este=True)
        self.assertEqual(self.b.regras, [])
        self.assertEqual(self.b.db.execute("SELECT status FROM lancamentos WHERE id=?", (r["id"],)).fetchone()[0], "manual")

    def test_direcao_separa_entrada_de_saida_do_mesmo_socio(self):
        explicar_por_nome(self.b, "SOCIO TESTE", "Retirada da PJ", "renda")
        r = self.b.regras[0]
        self.assertEqual((r["match"], r["direcao"]), (SOCIO, "entrada"))


class Resumo(unittest.TestCase):
    def setUp(self):
        self.b = banco()
        self.b.cfg["cartoes"] = ["sicredi-master", "azul"]
        self.b.importar_extrato(gravar(extrato_txt(OUT)))
        explicar_por_nome(self.b, "SOCIO TESTE", "Retirada da PJ", "renda")
        explicar_por_nome(self.b, "CLIENTE X", "Honorários", "renda")
        explicar_por_nome(self.b, "ITAU", "Pagamento de cartão", "pagamento_cartao")
        explicar_por_nome(self.b, "Diarista", "Diarista", "despesa")
        explicar_por_nome(self.b, "Fulano Obra", "Obra", "despesa")

    def test_so_extrato(self):
        d = self.b.resumo("2026-10")
        self.assertEqual(d["entrou"], D("7000.00"))
        # mercado 150 + diarista 400 + obra 609 + pequeno 50 + tarifa 32
        self.assertEqual(d["gastou"], D("1241.00"))
        self.assertEqual(d["saldo"], D("5759.00"))
        # fatura (1000) + Itaú (800) = pagamento de cartão; Pix para si (300) = transferência
        self.assertEqual(d["fora_do_calculo"], {"pagamento_cartao": D("1800.00"), "transferencia": D("300.00")})
        self.assertTrue(any("faltam faturas: sicredi-master, azul" in a for a in d["avisos"]))

    def test_unifica_fatura_sem_duplicar_pagamento(self):
        antes = self.b.resumo("2026-10")["gastou"]
        r = self.b.importar_fatura(gravar(montar(RESUMO_B, LINHAS_B, minimo="R$ 250,00"), "fat.csv"), "sicredi-master")
        self.assertEqual(r["novos"], 11 - 1 + 1)  # sem 'Pag Fat' + encargos não detalhados
        d = self.b.resumo("2026-10")
        # positivos da fatura (622,50) + encargos não detalhados (30,00)
        self.assertEqual(d["gastou"] - antes, D("652.50"))
        self.assertEqual(d["fora_do_calculo"]["pagamento_cartao"], D("1800.00"))  # pagamento só uma vez
        self.assertTrue(any("faltam faturas: azul" in a for a in d["avisos"]))
        self.assertFalse(any("sicredi-master" in a for a in d["avisos"]))

    def test_fatura_que_nao_concilia_nao_importa_nada(self):
        ruim = dict(RESUMO_B, brasil="R$ 999,00", total="R$ 1.470,00")
        with self.assertRaises(sf.ConciliacaoError):
            self.b.importar_fatura(gravar(montar(ruim, LINHAS_B), "ruim.csv"), "sicredi-master")
        self.assertEqual(self.b.db.execute("SELECT COUNT(*) FROM lancamentos WHERE origem LIKE 'fatura:%'").fetchone()[0], 0)

    def test_reimportar_fatura_nao_duplica(self):
        arq = gravar(montar(RESUMO_B, LINHAS_B), "fat.csv")
        self.b.importar_fatura(arq, "sicredi-master")
        self.assertTrue(self.b.importar_fatura(arq, "sicredi-master")["ja_importado"])

    def test_base_compra_leva_a_vista_para_mes_da_compra(self):
        self.b.cfg["base_cartao"] = "compra"
        self.b.importar_fatura(gravar(montar(RESUMO_B, LINHAS_B), "fat.csv"), "sicredi-master")
        meses = {r[0] for r in self.b.db.execute(
            "SELECT DISTINCT mes_ref FROM lancamentos WHERE descricao LIKE 'SUPREMA%'")}
        self.assertEqual(meses, {"2026-09"})   # compra de 15/09 vai para setembro
        parc = self.b.db.execute("SELECT mes_ref FROM lancamentos WHERE descricao LIKE 'SOL INDUSTRI%'").fetchone()[0]
        self.assertEqual(parc, "2026-10")      # parcela fica no mês da fatura


class Recorrencia(unittest.TestCase):
    def test_detecta_recorrentes(self):
        b = banco()
        b.importar_extrato(gravar(extrato_txt(OUT)))
        b.importar_extrato(gravar(extrato_txt(NOV, periodo="01/11/2026 a 30/11/2026"), "n.csv"))
        chaves = {x["chave"]: x for x in b.recorrencias()}
        self.assertIn(DIARISTA, chaves)
        self.assertEqual(chaves[DIARISTA]["media_mes"], D("410.00"))   # (400 + 420) / 2
        self.assertIn(SOCIO, chaves)
        self.assertNotIn("66666666666", chaves)                         # só um mês


class Cli(unittest.TestCase):
    def rodar(self, pasta, *args):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = app.main(["--dados", str(pasta), *args])
        return rc, buf.getvalue()

    def test_config_aceita_varios_cartoes_e_documentos(self):
        d = tempfile.mkdtemp()
        self.rodar(d, "config", "--cartao", "a", "--cartao", "b", "--documento", EU, "--documento", SOCIO)
        cfg = motor.Banco(d).cfg
        self.assertEqual(cfg["cartoes"], ["a", "b"])
        self.assertEqual(cfg["meus_documentos"], sorted([EU, SOCIO]))

    def test_fluxo_completo_importar_explicar_resumo(self):
        d = tempfile.mkdtemp()
        self.rodar(d, "config", "--documento", EU)
        rc, out = self.rodar(d, "importar-extrato", str(gravar(extrato_txt(OUT))))
        self.assertEqual(rc, 0)
        self.assertIn("conciliado", out)
        rc, out = self.rodar(d, "pendentes")
        self.assertIn("o que é?", out)
        self.assertNotIn(ITAU, out)            # documentos longos saem mascarados
        id_obra = out.split("Fulano Obra")[0].splitlines()[-1].split()[0]
        rc, out = self.rodar(d, "explicar", id_obra, "Obra")
        self.assertIn("regra congelada", out)
        rc, out = self.rodar(d, "resumo", "2026-10")
        self.assertIn("Obra", out)


if __name__ == "__main__":
    unittest.main()
