"""Leitor do extrato da conta Sicredi (CSV com ';').

Formato: linha de identificação/período, depois `Data;Descrição;Documento;Valor;Saldo`,
primeira linha `SALDO ANTERIOR`, valores em pt-BR sem "R$". A identificação do associado
é descartada. Conciliação obrigatória: o saldo corrente precisa bater linha a linha.
"""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path

import sicredi_fatura as sf


class ExtratoError(Exception):
    """Extrato não concilia (linha faltando, duplicada ou valor errado)."""


@dataclass
class LinhaExtrato:
    data: date
    descricao: str
    doc: str
    valor: Decimal
    saldo: Decimal


@dataclass
class Extrato:
    inicio: date | None
    fim: date | None
    saldo_anterior: Decimal
    saldo_final: Decimal
    linhas: list[LinhaExtrato]


def ler_extrato(caminho: str | Path) -> Extrato:
    texto = Path(caminho).read_text(encoding="utf-8-sig")
    rows = [[c.strip() for c in r] for r in csv.reader(texto.splitlines(), delimiter=";")]
    ini = next((i for i, c in enumerate(rows)
                if len(c) >= 5 and sf._sem_acento(c[0]) == "data" and sf._sem_acento(c[4]) == "saldo"), None)
    if ini is None:
        raise ExtratoError("cabeçalho 'Data;Descrição;Documento;Valor;Saldo' não encontrado")

    periodo = re.search(r"(\d{2}/\d{2}/\d{4})\s*a\s*(\d{2}/\d{2}/\d{4})", " ".join(";".join(r) for r in rows[:ini]))
    saldo_ant = None
    linhas: list[LinhaExtrato] = []
    for r in rows[ini + 1:]:
        r = (r + [""] * 5)[:5]
        data, desc, doc, valor, saldo = r
        if not data and "saldo anterior" in sf._sem_acento(desc):
            saldo_ant = sf.parse_valor(saldo)
            continue
        if not data or not valor:
            continue
        linhas.append(LinhaExtrato(sf.parse_data(data), sf._limpo(desc), doc, sf.parse_valor(valor),
                                   sf.parse_valor(saldo)))
    if saldo_ant is None:
        raise ExtratoError("linha SALDO ANTERIOR não encontrada")

    erros, corrente = [], saldo_ant
    for n, l in enumerate(linhas, 1):
        esperado = corrente + l.valor
        if esperado != l.saldo:
            erros.append(f"lançamento {n} ({l.data:%d/%m}): saldo informado {l.saldo}, esperado {esperado} "
                         f"(diferença {l.saldo - esperado})")
        corrente = l.saldo  # segue o saldo informado para localizar cada ruptura
    if erros:
        mais = f" (+{len(erros) - 5} outras)" if len(erros) > 5 else ""
        raise ExtratoError("extrato não concilia: " + "; ".join(erros[:5]) + mais)

    if periodo:
        ini_p, fim_p = sf.parse_data(periodo.group(1)), sf.parse_data(periodo.group(2))
    else:
        ini_p = min((l.data for l in linhas), default=None)
        fim_p = max((l.data for l in linhas), default=None)
    return Extrato(ini_p, fim_p, saldo_ant, corrente, linhas)
