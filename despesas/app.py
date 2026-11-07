"""CLI do app de despesas. Uso: python3 -I app.py [--dados PASTA] COMANDO ...

  importar-extrato ARQ [--conta sicredi-pf]       importar-fatura ARQ --cartao NOME
  pendentes                                        explicar ID "Categoria" [--tipo T] [--so-este] [--valor-exato]
  resumo AAAA-MM                                   acumulado AAAA
  lancar DD/MM/AAAA VALOR "Categoria" "descrição" [--tipo renda]      (dinheiro, outro banco)
  recorrencias
  config [--documento CPF] [--cartao NOME] [--limite N] [--base fatura|compra]
         [--esperado "Categoria|Nome|VALOR"]
Dados em despesas/dados/ (fora do git).
"""
import argparse
import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # necessário sob `python3 -I`

import extrato_sicredi as ex
import motor
import sicredi_fatura as sf


def _valor(s: str) -> Decimal:
    """'609,00' | '1.234,56' | '609.00' -> Decimal (ponto só é milhar quando há vírgula)."""
    return Decimal(s.replace(".", "").replace(",", ".") if "," in s else s)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="app.py")
    p.add_argument("--dados", default=str(Path(__file__).resolve().parent / "dados"))
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("importar-extrato"); a.add_argument("arq"); a.add_argument("--conta", default="sicredi-pf")
    a = sub.add_parser("importar-fatura"); a.add_argument("arq"); a.add_argument("--cartao", required=True)
    sub.add_parser("pendentes")
    a = sub.add_parser("explicar"); a.add_argument("id"); a.add_argument("categoria")
    a.add_argument("--tipo", default="despesa"); a.add_argument("--nota", default="")
    a.add_argument("--so-este", action="store_true"); a.add_argument("--valor-exato", action="store_true")
    a = sub.add_parser("resumo"); a.add_argument("mes")
    a = sub.add_parser("acumulado"); a.add_argument("ano")
    a = sub.add_parser("lancar"); a.add_argument("data"); a.add_argument("valor"); a.add_argument("categoria")
    a.add_argument("descricao"); a.add_argument("--tipo", default="despesa")
    sub.add_parser("recorrencias")
    a = sub.add_parser("config"); a.add_argument("--documento", action="append"); a.add_argument("--cartao", action="append")
    a.add_argument("--limite"); a.add_argument("--base", choices=("fatura", "compra")); a.add_argument("--esperado", action="append")
    args = p.parse_args(argv)
    b = motor.Banco(args.dados)
    try:
        if args.cmd == "importar-extrato":
            r = b.importar_extrato(args.arq, args.conta)
            print("arquivo já importado antes; nada a fazer" if r["ja_importado"] else
                  f"extrato {r['inicio']:%d/%m/%Y} a {r['fim']:%d/%m/%Y}: {r['novos']} novos, {r['duplicados']} repetidos "
                  f"(saldo {sf._brl(r['saldo_anterior'])} -> {sf._brl(r['saldo_final'])}, conciliado)")
        elif args.cmd == "importar-fatura":
            r = b.importar_fatura(args.arq, args.cartao)
            if r["ja_importado"]:
                print("arquivo já importado antes; nada a fazer")
            else:
                print(f"fatura venc. {r['vencimento']:%d/%m/%Y} ({sf._brl(r['total_fatura'])}): "
                      f"{r['novos']} novos, {r['duplicados']} repetidos, conciliada")
                for av in r["avisos"]:
                    print(f"  ! {sf.mascarar(av)}")
        elif args.cmd == "pendentes":
            grupos = {}
            for r in b.pendentes():  # uma pergunta por estabelecimento/pessoa; a explicação vale para todos
                g = grupos.setdefault(r["chave"], {"r": r, "n": 0, "total": motor.ZERO})
                g["n"] += 1
                g["total"] += abs(Decimal(r["valor"]))
            for g in grupos.values():
                r, v = g["r"], abs(Decimal(g["r"]["valor"]))
                extra = f"  (+{g['n'] - 1} iguais, total {sf._brl(g['total'])})" if g["n"] > 1 else ""
                print(f"{r['id'][:8]}  {r['data']}  {sf._brl(v):>14}  {sf.mascarar(r['descricao'])}{extra}  <- o que é?")
            print(f"{len(grupos)} a explicar" if grupos else "nada a explicar")
        elif args.cmd == "explicar":
            n = b.explicar(args.id, args.categoria, args.tipo, args.nota, args.so_este, args.valor_exato)
            print(f"ok: {n} lançamento(s) atualizado(s)" + ("" if args.so_este else "; regra congelada para os próximos envios"))
        elif args.cmd == "resumo":
            print(motor.texto_resumo(b.resumo(args.mes)))
        elif args.cmd == "acumulado":
            print(motor.texto_acumulado(b.acumulado(args.ano)))
        elif args.cmd == "lancar":
            d, m, y = map(int, args.data.split("/"))
            b.lancar(motor.date(y, m, d), _valor(args.valor), args.categoria, args.descricao, args.tipo)
            print("lançado")
        elif args.cmd == "recorrencias":
            for x in b.recorrencias():
                print(f"{sf.mascarar(x['nome'])[:34]:<36}{x['cat'][:26]:<28}{len(x['meses'])} meses  média {sf._brl(x['media_mes'])}")
        elif args.cmd == "config":
            if args.documento: b.cfg["meus_documentos"] = sorted(set(b.cfg["meus_documentos"]) | set(args.documento))
            if args.cartao: b.cfg["cartoes"] = sorted(set(b.cfg["cartoes"]) | set(args.cartao))
            if args.limite: b.cfg["limite_pergunta"] = args.limite
            if args.base: b.cfg["base_cartao"] = args.base
            for e in args.esperado or []:
                cat, nome, valor = e.split("|")
                b.cfg["esperados"] = [x for x in b.cfg["esperados"] if x["categoria"] != cat] + \
                                     [{"categoria": cat, "nome": nome, "valor": str(_valor(valor))}]
            b.salvar_config()
            print(f"config: {len(b.cfg['meus_documentos'])} documento(s) próprio(s), cartões {b.cfg['cartoes']}, "
                  f"{len(b.cfg['esperados'])} valor(es) esperado(s), pergunta a partir de R$ {b.cfg['limite_pergunta']}, "
                  f"cartão por {b.cfg['base_cartao']}")
    except (ex.ExtratoError, sf.ConciliacaoError) as e:
        print(f"CONCILIAÇÃO FALHOU, nada foi importado: {sf.mascarar(str(e))}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"erro: {e}", file=sys.stderr)
        return 1
    finally:
        b.db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
