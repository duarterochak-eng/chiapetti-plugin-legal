"""Taxonomia de categorias do titular. Primeira que casar vence; a ordem importa.

Formato "Grupo › Item": o resumo soma por grupo e detalha por item. O que não casar aqui
vira pergunta ("A classificar") e a resposta do titular é congelada como regra.
"""
from __future__ import annotations

import sicredi_fatura as sf

SEP = " › "

TAXONOMIA: list[tuple[str, tuple[str, ...]]] = [
    ("Financeiro › Tarifas bancárias", ("cesta de relacionamento", "iof adicional", "iof basico",
                                        "juros utiliz", "seguro prestamista")),
    # Casa
    ("Casa › Material de limpeza (Mercado Livre)", ("mercadolivre", "mercado livre")),
    ("Casa › Luz", ("energisa",)),
    ("Casa › Internet", ("lci tel",)),
    ("Casa › Lavanderia", ("lavanderia",)),
    ("Casa › Condomínio", ("ecovil", "condomin")),
    ("Casa › Mercado", ("supermerc", "atacad", "hortifruti", "mercearia")),
    # Carro
    ("Carro › Lavador", ("lavajato", "lava jato", "lavego")),
    ("Carro › Combustível", ("baratao", "posto", "combust", "ipiranga", "shell")),
    ("Carro › Oficina/Toyota", ("toyota", "oficina", "auto center", "mecanica")),
    ("Carro › IPVA/Licenciamento", ("detran", "ipva", "licenciamento")),
    ("Carro › Ótica", ("otica",)),
    ("Carro › Seguro", ("seguro auto", "porto seguro", "tokio marine")),
    # Categorias próprias
    ("Loja maçônica", ("augusta e respeitav",)),
    ("Unimed", ("unimed",)),
    ("Farmácia", ("farma", "pharmacia", "drog", "drugstore", "biomanip", "formula certa", "therapeutic")),
    ("Kart", ("kart",)),
    ("Bar e restaurante", ("viracopo", "vira copo", "la vie", "taboo", "steak", "restaur", "ifood", "lanche",
                           "pizza", "burger", "padaria", "cafe", "acai", "sorvete", "degustare", "convenienc",
                           "churrasc", "gaucho", "boteco")),
    # Mensalidades (assinaturas): um item por serviço, total no grupo
    ("Mensalidades › Netflix", ("netflix",)),
    ("Mensalidades › Jus Brasil", ("jusbrasil", "jus brasil")),
    ("Mensalidades › Apple", ("apple com",)),
    ("Mensalidades › Microsoft", ("microsoft",)),
    ("Mensalidades › iLovePDF", ("ilovepdf", "i love pdf")),
    ("Mensalidades › Google", ("google",)),
    ("Mensalidades › Claude (Anthropic)", ("anthropic", "claude")),
    ("Mensalidades › Spotify", ("spotify",)),
    # Extraordinárias (pontuais)
    ("Extraordinárias › Limpeza de ar-condicionado", ("limpeza de ar", "limpesq")),
    # Fora da lista do titular, mantido por ser óbvio (confirmar)
    ("Seguro de vida (Prudential)", ("prudential",)),
]


def sugerir(descricao: str) -> str | None:
    d = " ".join(sf._sem_acento(descricao).split())
    return next((cat for cat, ks in TAXONOMIA if any(k in d for k in ks)), None)


def grupo_item(categoria: str) -> tuple[str, str]:
    g, sep, item = categoria.partition(SEP)
    return (g, item) if sep else (categoria, categoria)
