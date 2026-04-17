---
name: brief
description: Gera briefings contextuais para trabalho jurídico — síntese diária, pesquisa temática, ou resposta a incidente. Use ao iniciar o dia e precisar de uma varredura de itens juridicamente relevantes em e-mail, agenda e contratos; ao pesquisar questão jurídica específica em fontes internas; ou quando uma situação em desenvolvimento (incidente de dados, ameaça de litígio, consulta regulatória) exigir contextualização rápida.
argument-hint: "[diario | tema <consulta> | incidente]"
---

# /brief — Briefing Jurídico

> Consulte [CONNECTORS.md](../../CONNECTORS.md).

Gera briefings contextuais para o trabalho jurídico. Três modos: diário, temático e de incidente.

**Vedação à alucinação.** Nenhum fato, dispositivo, jurisprudência ou precedente é citado sem base verificável em fonte conectada ou documento anexo. Diante de lacuna, reportar expressamente "informação não localizada".

## Invocação

```
/brief diario                      # Síntese matinal de itens juridicamente relevantes
/brief tema [consulta]             # Pesquisa interna sobre questão jurídica específica
/brief incidente [tópico]          # Briefing rápido sobre situação em desenvolvimento
```

## Modo 1 — Briefing diário

Varredura da manhã. Consultar `~~email`, `~~agenda`, `~~armazenamento`, `~~CLM`, `~~gestão` e identificar:

- **Prazos processuais** em curso e a vencer nos próximos 7 dias (considerar feriados forenses, recesso art. 220 CPC, suspensões ex art. 313 CPC)
- **Audiências e reuniões** do dia/semana (diligenciar, AIJ, sustentação oral, audiência de conciliação, reuniões com cliente)
- **Publicações** no DJe, intimações eletrônicas via PJe/e-SAJ/Projudi (via `~~email` ou integração com `~~tribunal`)
- **Consultas internas** pendentes (negocial, contratual, consultivo)
- **Alertas regulatórios** — publicações relevantes (ANPD, CVM, BACEN, CADE, ANS conforme o setor)
- **Contratos com renovação/vencimento próximo** no `~~CLM`
- **Fato relevante** no mercado (se houver companhia aberta na base de clientes — CVM Res. 44/2021)

### Saída

```
## Briefing Jurídico — [data]

### Prazos processuais críticos (próximos 7 dias)
| Processo | Peça | Vencimento | Responsável |
|----------|------|------------|-------------|

### Audiências e reuniões do dia
- [horário] — [natureza] — [processo/cliente] — [observações]

### Publicações e intimações
- [órgão] — [processo] — [conteúdo sintetizado]

### Consultas pendentes
[—]

### Alertas regulatórios / novidades legislativas
[—]

### Contratos com renovação/vencimento próximo
[—]

### Outros itens relevantes
[—]

### Lacunas
[Itens que precisam de verificação manual — explicitados]
```

## Modo 2 — Briefing temático

Pesquisa interna sobre questão jurídica específica. Percorre `~~armazenamento`, `~~email`, `~~CLM`, `~~gestão` para localizar memoriais, pareceres, precedentes internos, minutas, e-mails relevantes, contratos com cláusulas análogas.

**Importante.** O briefing temático é **pesquisa interna**, não elaboração de parecer jurídico autônomo. Se o usuário precisar de análise jurídica externa (jurisprudência de tribunais, doutrina), a IA **recomenda pesquisa dedicada** (STJ, STF, TST, TRF, TJ, periódicos jurídicos), **sem inventar**.

### Saída

```
## Briefing Temático — [consulta]

### Síntese da questão
[Reformulação técnica do que está sendo pesquisado]

### Fontes internas localizadas
| Documento | Tipo | Relevância | Caminho |
|-----------|------|------------|---------|

### Conteúdo relevante — trechos e referências
[Citações literais, com origem]

### Posicionamento interno anterior (se houver)
[Se a casa já tratou da matéria em parecer/memorial]

### Lacunas e recomendações de pesquisa externa
[Fontes a serem consultadas — STJ, STF, TST, doutrina — sem citações inventadas]
```

## Modo 3 — Briefing de incidente

Situação em desenvolvimento. Contexto típico: (i) incidente de segurança envolvendo dados pessoais (art. 48 LGPD), (ii) notificação de autoridade (oficial de justiça, Polícia, MP, ANPD, CADE, RFB), (iii) ameaça de litígio (notificação extrajudicial, protesto), (iv) crise reputacional, (v) investigação interna.

Varredura imediata em `~~email`, `~~armazenamento`, `~~chat`, `~~CLM`, `~~CRM` para:

- Reconstituir a cronologia do incidente
- Identificar documentos e contratos potencialmente impactados
- Identificar pessoas envolvidas
- Localizar políticas e procedimentos internos aplicáveis
- Identificar obrigações regulatórias de comunicação (ex.: comunicação de incidente à ANPD e aos titulares nos termos do art. 48 LGPD; Resoluções ANPD 2/2022 e 15/2024)

### Saída

```
## Briefing de Incidente — [natureza / título]
**Data/hora de ciência**: [—]
**Prazos regulatórios eventuais**: [—]

### Cronologia reconstituída
[Linha do tempo com fonte de cada fato]

### Documentos e contratos envolvidos
[—]

### Pessoas envolvidas
[—]

### Obrigações imediatas de comunicação / reporte
[Com base legal — LGPD, BACEN, CVM, setorial]

### Riscos imediatos
[Classificação preliminar; recomendar `/avaliar-risco` para aprofundamento]

### Próximos passos recomendados
[—]

### Lacunas
[—]
```

## Observações

- **Linguagem técnica, formal, PT-BR culto.**
- Todo dado factual é acompanhado da **fonte** (documento, e-mail, sistema, data).
- Em ambiente com sigilo, marcar o briefing como **"Matéria submetida a sigilo profissional — uso interno"**.
- Se surgirem riscos sérios (LGPD, penal, regulatório), acionar `/avaliar-risco` e `/verificar-compliance`.
