import sys
import tempfile
import unittest
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import io  # noqa: E402
import warnings  # noqa: E402

warnings.simplefilter("ignore", ResourceWarning)  # conexões sqlite de teste são descartáveis
from contextlib import redirect_stdout  # noqa: E402
from datetime import date  # noqa: E402

import app  # noqa: E402
import extrato_sicredi as ex  # noqa: E402
import motor  # noqa: E402
import sicredi_fatura as sf  # noqa: E402
from test_sicredi_fatura import LINHAS_A, LINHAS_B, RESUMO_A, RESUMO_B, montar  # noqa: E402

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
        self.assertEqual(self.t["CESTA DE RELACIONAMENTO"]["categoria"], "Financeiro › Tarifas bancárias")
        mercado = next(r for d, r in self.t.items() if "DEL MORO" in d)
        self.assertEqual(mercado["categoria"], "Casa › Mercado")

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


class Taxonomia(unittest.TestCase):
    CASOS = {
        "PAGAMENTO PIX 03467321000199 ENERGISA MT": "Casa › Luz",
        "LIQUIDACAO BOLETO SICREDI 09144880000144 LCI TEL": "Casa › Internet",
        "LavanderiaRibeiro": "Casa › Lavanderia",
        "SUPERMERCADOS MACHAD": "Casa › Mercado",
        "MERCADOLIVRE MERCAD": "Casa › Material de limpeza (Mercado Livre)",
        "LavaJatoMoradaDo": "Carro › Lavador",
        "AUTO POSTO AVANTI": "Carro › Combustível",
        "PGTO SEFAZ/DETRAN MT": "Carro › IPVA/Licenciamento",
        "PAGAMENTO PIX 10374305000117 AUGUSTA E RESPEITAV": "Loja maçônica",
        "LIQUIDACAO BOLETO SICREDI 73967085000155 UNIMED": "Unimed",
        "SUPREMA FARMA SORRIS": "Farmácia",
        "PHARMACIA THERAPEUTI": "Farmácia",
        "ViraCopoPromotora": "Bar e restaurante",
        "COMPRA DEBITO MASTER CONVENIENCIA ROTA DO S SORR": "Bar e restaurante",
        "APPLE COM/BILL": "Mensalidades › Apple",
        "Microsoft Microsoft": "Mensalidades › Microsoft",
        "ANTHROPIC CLAUDE SU": "Mensalidades › Claude (Anthropic)",
        "SEGURO PRESTAMISTA": "Financeiro › Tarifas bancárias",
    }

    def test_sugestoes(self):
        for desc, cat in self.CASOS.items():
            self.assertEqual(motor.sugerir(desc), cat, desc)

    def test_nao_reconhece_o_resto(self):
        for desc in ("MM QUIMICA PRODUTOS", "JIM COM AVANCCE", "MAGAZINE LUIZA SA", "SOL INDUSTRI Cartao"):
            self.assertIsNone(motor.sugerir(desc), desc)

    def test_grupo_item(self):
        self.assertEqual(categorias_grupo("Casa › Luz"), ("Casa", "Luz"))
        self.assertEqual(categorias_grupo("Farmácia"), ("Farmácia", "Farmácia"))


def categorias_grupo(c):
    import categorias
    return categorias.grupo_item(c)


class Grupos(unittest.TestCase):
    def setUp(self):
        self.b = banco()
        self.b.importar_extrato(gravar(extrato_txt(OUT)))
        self.b.importar_fatura(gravar(montar(RESUMO_B, LINHAS_B), "fat.csv"), "sicredi-master")

    def test_resumo_por_grupo_com_itens(self):
        g = self.b.resumo("2026-10")["gastou_por_grupo"]
        self.assertEqual(g["Casa"]["itens"]["Mercado"], D("150.00"))
        self.assertEqual(g["Farmácia"]["total"], D("170.00"))
        self.assertEqual(g["Mensalidades"]["itens"], {"Claude (Anthropic)": D("40.00")})
        self.assertEqual(g["Financeiro"]["itens"]["Encargos de cartão"], D("32.50") + D("30.00"))  # itemizados + não detalhados
        self.assertNotIn("Casa", {k for k in g if g[k]["total"] < 0})

    def test_valor_exato_distingue_prestacao_de_repasse_ao_mesmo_favorecido(self):
        b = banco()
        extra = [("02/10/2026", f"TRANSF ENTRE CONTAS {SOCIO} SOCIO TESTE", "SI1", "-2509.00"),
                 ("03/10/2026", f"TRANSF ENTRE CONTAS {SOCIO} SOCIO TESTE", "SI2", "-500.00")]
        b.importar_extrato(gravar(extrato_txt(extra), "x.csv"))
        pres = b.db.execute("SELECT id FROM lancamentos WHERE valor='-2509.00'").fetchone()["id"]
        b.explicar(pres, "Casa › Condomínio (prestação)", valor_exato=True)
        cats = {r["valor"]: r["categoria"] for r in b.db.execute("SELECT valor, categoria FROM lancamentos")}
        self.assertEqual(cats["-2509.00"], "Casa › Condomínio (prestação)")
        self.assertEqual(cats["-500.00"], "A classificar")           # o outro valor não é capturado
        b.importar_extrato(gravar(extrato_txt([("02/11/2026", f"TRANSF ENTRE CONTAS {SOCIO} SOCIO TESTE", "SI3", "-2509.00")],
                                              periodo="01/11/2026 a 30/11/2026"), "y.csv"))
        nov = b.db.execute("SELECT categoria, status FROM lancamentos WHERE mes_ref='2026-11'").fetchone()
        self.assertEqual((nov["categoria"], nov["status"]), ("Casa › Condomínio (prestação)", "regra"))

    def test_esperado_gera_aviso_quando_falta(self):
        self.b.cfg["esperados"] = [{"categoria": "Casa › Condomínio (prestação)", "nome": "Prestação ao Juarez",
                                    "valor": "2509.00"}]
        av = self.b.resumo("2026-10")["avisos"]
        self.assertTrue(any("esperado e não encontrado: Prestação ao Juarez (R$ 2.509,00)" in a for a in av))
        self.b.lancar(date(2026, 10, 25), D("2509.00"), "Casa › Condomínio (prestação)", "Prestação (CEF Juarez)")
        av = self.b.resumo("2026-10")["avisos"]
        self.assertFalse(any("esperado" in a for a in av))

    def test_lancar_manual_entra_no_resumo(self):
        antes = self.b.resumo("2026-10")["gastou"]
        self.b.lancar(date(2026, 10, 20), D("100.00"), "Bar e restaurante", "churrasco em dinheiro")
        self.b.lancar(date(2026, 10, 20), D("100.00"), "Bar e restaurante", "churrasco em dinheiro")  # idempotente
        self.assertEqual(self.b.resumo("2026-10")["gastou"] - antes, D("100.00"))

    def test_acumulado(self):
        self.b.importar_extrato(gravar(extrato_txt(NOV, periodo="01/11/2026 a 30/11/2026"), "n.csv"))
        a = self.b.acumulado("2026")
        self.assertEqual([m["mes"] for m in a["meses"]], ["2026-10", "2026-11"])
        self.assertEqual(a["meses"][1]["acumulado"], a["meses"][0]["saldo"] + a["meses"][1]["saldo"])
        self.assertEqual(a["gastou"], sum(m["gastou"] for m in a["meses"]))
        self.assertIn("Casa", a["grupos"])


class DividaEParcelas(unittest.TestCase):
    CAT = "Casa › Condomínio (prestação)"

    def setUp(self):
        self.b = banco()
        self.b.importar_extrato(gravar(extrato_txt(OUT)))
        self.b.cfg["esperados"] = [{"categoria": self.CAT, "nome": "Prestação ao Juarez", "valor": "2500.00",
                                    "desde": "2026-08"}]

    def aviso_aberto(self, mes="2026-10"):
        return next((a for a in self.b.resumo(mes)["avisos"] if a.startswith("em aberto")), None)

    def test_divida_acumula_meses_devidos(self):
        a = self.aviso_aberto()
        self.assertIn("R$ 7.500,00", a)           # ago, set, out x 2.500
        self.assertIn("3 mês(es) desde 2026-08", a)

    def test_pagamento_abate_a_divida(self):
        self.b.lancar(date(2026, 9, 25), D("2500.00"), self.CAT, "Prestação (CEF Juarez)")
        self.assertIn("R$ 5.000,00", self.aviso_aberto())

    def test_quitando_tudo_some_o_aviso(self):
        self.b.lancar(date(2026, 10, 25), D("7500.00"), self.CAT, "Prestação atrasada (CEF Juarez)")
        self.assertIsNone(self.aviso_aberto())

    def test_sem_desde_nao_gera_divida(self):
        self.b.cfg["esperados"][0].pop("desde")
        self.assertIsNone(self.aviso_aberto())

    def test_parcelas_a_vencer_e_separacao_como_obra(self):
        self.b.importar_fatura(gravar(montar(RESUMO_B, LINHAS_B), "fat.csv"), "sicredi-master")
        ps = self.b.parcelas()
        self.assertEqual(len(ps), 1)
        self.assertEqual((ps[0]["n"], ps[0]["t"], ps[0]["restam"], ps[0]["saldo"]), (4, 10, 6, D("600.00")))
        self.assertEqual(self.b.resumo("2026-10")["parcelas_a_vencer"], {"A classificar": D("600.00")})
        # avisa uma vez que é obra: vale para todas as parcelas, passadas e futuras
        explicar_por_nome(self.b, "SOL INDUSTRI", "Extraordinárias › Obra do novo escritório")
        self.assertEqual(self.b.resumo("2026-10")["parcelas_a_vencer"],
                         {"Extraordinárias › Obra do novo escritório": D("600.00")})
        g = self.b.resumo("2026-10")["gastou_por_grupo"]["Extraordinárias"]["itens"]
        self.assertEqual(g["Obra do novo escritório"], D("100.00"))     # só a parcela do mês

    def test_parcela_quitada_nao_entra(self):
        self.b.importar_fatura(gravar(montar(RESUMO_A, LINHAS_A), "a.csv"), "sicredi-master")
        nomes = [p["nome"] for p in self.b.parcelas()]
        self.assertIn("MERCADOLIVRE MERCAD", nomes)   # 2/3 -> resta 1
        self.assertNotIn("FOSSIL", nomes)              # 10/10 -> nada a vencer


class ForaDoNormal(unittest.TestCase):
    def setUp(self):
        self.b = banco()
        for mes, v in (("07", "400"), ("08", "400"), ("09", "1000"), ("10", "450")):
            self.b.lancar(date(2026, int(mes), 10), D(v), "Bar e restaurante", "Padaria do Ze")
        self.b.lancar(date(2026, 9, 12), D("300"), "Bar e restaurante", "Lugar Novo")       # sem histórico
        self.b.lancar(date(2026, 8, 12), D("100"), "Bar e restaurante", "Lugar Recente")
        self.b.lancar(date(2026, 9, 12), D("900"), "Bar e restaurante", "Lugar Recente")    # só 1 mês antes

    def test_avisa_quando_passa_muito_do_habitual(self):
        (x,) = self.b.fora_do_normal("2026-09")
        self.assertEqual((x["nome"], x["atual"], x["media"]), ("Padaria do Ze", D("1000"), D("400.00")))
        self.assertTrue(any("fora do normal: Padaria do Ze" in a for a in self.b.resumo("2026-09")["avisos"]))

    def test_variacao_pequena_nao_avisa(self):
        self.assertEqual(self.b.fora_do_normal("2026-10"), [])

    def test_sem_historico_suficiente_nao_avisa(self):
        nomes = [x["nome"] for x in self.b.fora_do_normal("2026-09")]
        self.assertNotIn("Lugar Novo", nomes)
        self.assertNotIn("Lugar Recente", nomes)


class CopiaDeSeguranca(unittest.TestCase):
    def test_ida_e_volta_preserva_tudo(self):
        a = banco()
        a.importar_extrato(gravar(extrato_txt(OUT)))
        a.importar_fatura(gravar(montar(RESUMO_B, LINHAS_B), "fat.csv"), "sicredi-master")
        explicar_por_nome(a, "SOCIO TESTE", "Retirada da PJ", "renda")
        explicar_por_nome(a, "Fulano Obra", "Extraordinárias › Obra", "despesa")
        a.cfg["cartoes"] = ["sicredi-master", "azul"]
        pasta = Path(tempfile.mkdtemp())
        n = a.salvar_snapshot(pasta)
        self.assertEqual(n["lancamentos"], a.db.execute("SELECT COUNT(*) FROM lancamentos").fetchone()[0])
        for nome in ("lancamentos.csv", "importacoes.csv", "regras.json", "config.json"):
            self.assertTrue((pasta / nome).exists(), nome)

        b = motor.Banco(tempfile.mkdtemp())          # máquina nova, sem nada
        b.restaurar_snapshot(pasta)
        self.assertEqual(b.regras, a.regras)
        self.assertEqual(b.cfg["cartoes"], ["sicredi-master", "azul"])
        for mes in ("2026-10",):
            ra, rb = a.resumo(mes), b.resumo(mes)
            for k in ("entrou", "gastou", "saldo", "gastou_por_grupo", "fora_do_calculo", "parcelas_a_vencer"):
                self.assertEqual(ra[k], rb[k], k)
        self.assertEqual(b.parcelas(), a.parcelas())

    def test_depois_de_restaurar_nao_reimporta_nem_duplica(self):
        a = banco()
        arq = gravar(extrato_txt(OUT))
        a.importar_extrato(arq)
        pasta = Path(tempfile.mkdtemp())
        a.salvar_snapshot(pasta)
        b = motor.Banco(tempfile.mkdtemp())
        b.restaurar_snapshot(pasta)
        self.assertTrue(b.importar_extrato(arq)["ja_importado"])
        extra = OUT[:5] + [("12/10/2026", "COMPRA DEBITO MASTER PADARIA X", "CM02", "-20.00")]
        r = b.importar_extrato(gravar(extrato_txt(extra), "g.csv"))
        self.assertEqual((r["novos"], r["duplicados"]), (1, 5))

    def test_regra_restaurada_vale_para_novos_envios(self):
        a = banco()
        a.importar_extrato(gravar(extrato_txt(OUT)))
        explicar_por_nome(a, "ITAU", "Pagamento de cartão", "pagamento_cartao")
        pasta = Path(tempfile.mkdtemp())
        a.salvar_snapshot(pasta)
        b = motor.Banco(tempfile.mkdtemp())
        b.restaurar_snapshot(pasta)
        b.importar_extrato(gravar(extrato_txt(NOV, periodo="01/11/2026 a 30/11/2026"), "n.csv"))
        r = b.db.execute("SELECT tipo, status FROM lancamentos WHERE descricao LIKE '%ITAU%' AND mes_ref='2026-11'").fetchone()
        self.assertEqual((r["tipo"], r["status"]), ("pagamento_cartao", "regra"))

    def test_copia_incompleta_falha_com_clareza(self):
        with self.assertRaises(ValueError):
            motor.Banco(tempfile.mkdtemp()).restaurar_snapshot(tempfile.mkdtemp())


if __name__ == "__main__":
    unittest.main()
