---
name: review-contract
description: Revisa contrato cláusula a cláusula contra o playbook do escritório, apontando desvios, gerando sugestões de redação (red-lines) e análise de impacto. Use ao receber minuta de fornecedor/cliente, para análise cláusula a cláusula contra posições-padrão, ou ao preparar estratégia de negociação com prioridades e fallbacks. Ancorado no ordenamento brasileiro — CC/2002 (especialmente arts. 421-426 — função social, boa-fé objetiva), CDC quando aplicável, LGPD (DPA), Lei 9.307/96 (arbitragem), Lei 14.133/2021 (contratos administrativos).
argument-hint: "<contrato / minuta>"
---

# /revisar-contrato — Revisão Contratual

> Consulte [CONNECTORS.md](../../CONNECTORS.md).

Revisa minutas contratuais contra o playbook da casa, aponta desvios, elabora sugestões de redação e análise de impacto.

**Vedação à alucinação.** Nenhuma cláusula é sugerida com base em jurisprudência, súmula, enunciado ou doutrina que não tenha sido efetivamente localizada. Dispositivos legais são citados **apenas** quando efetivamente aplicáveis. Ausência de playbook é reportada, não presumida.

## Invocação

```
/revisar-contrato [arquivo / texto]
```

## Fluxo

### Fase 1 — Caracterização do contrato

- **Natureza** (prestação de serviços, compra e venda, cessão, licenciamento, franquia, distribuição, representação, locação, parceria, consórcio, M&A — compra de quotas/ações, agreements, JVA, SHA, consumo, administrativo — Lei 14.133/2021)
- **Partes** (qualificação, capacidade, representação)
- **Regime jurídico** — comum (CC), consumerista (CDC), administrativo (Lei 14.133/2021), trabalhista, internacional
- **Valor** (se pertinente)
- **Vigência**
- **Submissão eventual a regulação setorial** (BACEN, CVM, SUSEP, ANS, ANVISA, ANATEL, ANEEL, CADE)

### Fase 2 — Check-list estrutural (CC/2002 e legislação especial)

**Requisitos de validade** (art. 104 CC):
- Agente capaz (arts. 3º, 4º, 5º CC; capacidade de sociedades — LSA, CC)
- Objeto lícito, possível, determinado ou determinável
- Forma prescrita ou não defesa em lei (escritura pública quando exigível — ex.: alienação imobiliária > 30 salários-mínimos; art. 108 CC)

**Princípios contratuais**:
- Autonomia privada (art. 421 CC)
- Função social do contrato (art. 421 CC)
- Boa-fé objetiva (art. 422 CC) — deveres anexos: informação, lealdade, cooperação, proteção
- Equilíbrio contratual — teoria da imprevisão (art. 478 CC — onerosidade excessiva) e revisão (art. 317 CC)
- Probidade

**Cláusulas vedadas em geral**:
- Renúncia antecipada do aderente a direito resultante da natureza do negócio (art. 424 CC, em contratos de adesão)
- Cláusula exonerativa de dolo ou culpa grave (vedada pelo princípio geral de boa-fé — art. 422; analogia ao art. 51, I, CDC)
- Em relação de consumo — art. 51 CDC (rol não exaustivo): limitação de indenização, inversão do ônus da prova em desfavor do consumidor, foro de eleição que dificulte defesa do consumidor (Súm. 381 STJ — nulidade de ofício), cláusula-mandato, renúncia a direito

### Fase 3 — Análise cláusula a cláusula

#### Objeto e escopo
- Determinação precisa; exclusões expressas; critérios de mensuração de entrega/prestação.

#### Preço e pagamento
- Indexação (IPCA, IGP-M, INPC — atentar para obsolescência do IGP-M em contratos residenciais — Lei 14.010/2020 em contexto da pandemia)
- Reajuste (Lei 10.192/2001 — anualidade mínima para contratos em moeda nacional)
- Multa, juros de mora (art. 406 CC — taxa legal, discussão sobre SELIC vs. 1% a.m.; art. 591 CC — juros compostos vedados em contratos civis comuns, salvo instituições financeiras — Súm. 596 STF; Lei 4.595/64)
- Retenções tributárias (IR-fonte, ISS, PIS/COFINS, CSLL, INSS — Lei 9.430/96, IN RFB 1.234/2012)

#### Prazo e rescisão
- Vigência determinada / indeterminada
- Denúncia unilateral (art. 473 CC) — prazo razoável; em contratos de execução continuada com investimento vultoso, parágrafo único exige prazo compatível com a amortização
- Resolução por inadimplemento (art. 475 CC — direito alternativo entre resolução e cumprimento, cumulado com perdas e danos)
- Resilição bilateral (distrato — art. 472 CC; forma idêntica ao contrato; art. 473)
- Cláusula resolutiva expressa (art. 474 CC — opera de pleno direito); tácita (art. 475 — exige manifestação ou provimento judicial)

#### Limitação de responsabilidade
- Padrão do playbook (ex.: limite mútuo = 12 meses de valores pagos)
- **Não admissíveis**: exclusão por dolo/culpa grave (art. 422; analogia CDC 51, I); limite que torne o contrato inócuo (art. 424 em adesão); em consumo — art. 51, I
- **Danos indiretos / lucros cessantes** — cláusula limitativa é válida em contratos paritários; em consumo, a exclusão de lucros cessantes é cláusula abusiva quando priva o consumidor da reparação integral (art. 6º, VI, CDC)

#### Indenização (indemnification)
- Escopo (PI, dados, terceiros, material), mutualidade, teto, carve-outs (dolo, culpa grave, violação à LGPD — atentar à solidariedade do art. 42 LGPD entre controlador e operador)

#### Confidencialidade
- Prazo (2-5 anos padrão; indeterminado para segredo de indústria — art. 195 Lei 9.279/96)
- Escopo, exceções (informação pública, desenvolvida independentemente, recebida legitimamente de terceiro, exigida por autoridade)
- Retenção pós-término
- Consequências do descumprimento (multa, tutela específica)

#### LGPD / tratamento de dados pessoais
- **Papéis** (controlador, operador, cocontrolador — art. 5º e art. 37 LGPD)
- **DPA (Contrato de Tratamento de Dados)** — obrigatório quando operador trata dados em nome do controlador (art. 39)
- **Obrigações do operador**: seguir instruções do controlador; adotar medidas técnicas e administrativas (art. 46); notificar incidentes; subcontratação com anuência; devolver/eliminar ao término
- **Comunicação de incidente** à ANPD e aos titulares — "prazo razoável" (Res. ANPD 15/2024 e 2/2022); o DPA deve impor prazo interno entre operador e controlador
- **Transferência internacional** (arts. 33-36) — base legal específica
- **Direitos do titular** (art. 18) — responsabilidade da parte pertinente
- **Responsabilidade** — art. 42 (solidariedade controlador/operador); art. 43 (excludentes); art. 44 (responsabilidade objetiva — debate doutrinário)

#### Propriedade intelectual
- Titularidade (criação sob encomenda — art. 4º Lei 9.609/98 para software; art. 11 Lei 9.279/96 para invenção; art. 88 para obra do empregado)
- Licenciamento (exclusivo/não-exclusivo; território; prazo)
- Registro e manutenção

#### Anticorrupção / Compliance
- Declarações e garantias de conformidade (Lei 12.846/2013, FCPA, UK Bribery Act — conforme exposição internacional)
- Direito de auditoria (audit rights)
- Obrigação de comunicação de suspeitas
- Rescisão por descumprimento

#### Cessão e subcontratação
- Condições de anuência
- Responsabilidade solidária do cedente
- Comunicação prévia

#### Foro e lei aplicável
- Foro de eleição — art. 63 CPC (paritário); vedação em consumo art. 51, IV CDC; nulidade de ofício — Súm. 381 STJ
- Lei aplicável — LINDB arts. 9-10 (contratos internacionais); em contratos domésticos, lei brasileira
- Arbitragem — Lei 9.307/96; escolha de câmara (CAM-CCBC, CAMARB, CCI, AmCham, CIESP-FIESP); sede; idioma; nº de árbitros; regra processual; arbitrabilidade objetiva (direito patrimonial disponível — art. 1º Lei 9.307/96)

#### Disposições finais
- Notificações (canal e prazo)
- Novação (art. 360 CC)
- Integração contratual (merger clause)
- Independência das cláusulas (severability)
- Alterações (forma escrita)
- Tributos (atribuição de ônus fiscal)
- Casos fortuitos e força maior (art. 393 CC)

### Fase 4 — Consolidação

Produção de:
- **Relatório de revisão** com tabela cláusula × desvio × posição playbook × sugestão × prioridade
- **Red-lines** (sugestões de redação)
- **Nota de negociação** — argumentos para sustentar cada pedido

## Formato de saída

```
## Revisão Contratual — [contrato]
**Parte representada**: [—]
**Natureza**: [—]
**Valor**: R$ [—]
**Vigência**: [—]

### 1. Caracterização
[—]

### 2. Quadro-resumo de desvios
| # | Cláusula | Posição contraparte | Posição playbook | Desvio | Prioridade | Sugestão |
|---|---|---|---|---|---|---|
| 1 | Limitação de responsabilidade | ilimitada + lucros cessantes | mútua 12m | crítico | 1 | "A responsabilidade de cada parte..." |

### 3. Análise cláusula a cláusula (detalhada)
[Cláusula a cláusula, com fundamentação]

### 4. Red-lines sugeridas
[Texto proposto para cada cláusula problemática — integração com `~~suíte` para controle de alterações em .docx]

### 5. Prioridades de negociação
- **Crítico — não ceder**: [—]
- **Alto — ceder mediante contrapartida**: [—]
- **Médio — flexível**: [—]
- **Baixo — aceitável**: [—]

### 6. Riscos residuais
[—]

### 7. Aprovações internas exigidas
[Alçada; aprovação de LGPD; aprovação societária — art. 142 LSA se matéria de competência do Conselho]

### 8. Documentos anexos exigíveis
[DPA; anexo técnico; SLA; Termo de Sigilo]

### 9. Recomendação final
[Assinar conforme está / assinar após ajustes / não assinar / escalonar]

### 10. Lacunas
[—]
```

## Observações

- **Linguagem técnica, formal, PT-BR culto.**
- Quando o contrato for **de adesão**, aplicar o filtro do art. 424 CC e do CDC.
- Quando houver **relação de consumo**, aplicar integralmente o CDC.
- Quando houver **contratação com Administração Pública**, aplicar a Lei 14.133/2021 (nova lei de licitações), ou a Lei 8.666/93 para contratos ainda sob regime anterior (vigência até 2023/2024 conforme transição).
- **Documento DOCX** — integrar com `~~suíte` para gerar minuta com alterações rastreadas (track changes).
- **Revisão humana obrigatória** antes de qualquer envio ao cliente/contraparte.
- **Sigilo profissional** mantido — matéria submetida a sigilo.
