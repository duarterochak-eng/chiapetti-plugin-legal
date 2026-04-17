---
name: analise-processo-medio
description: Analisa processos judiciais ou administrativos de médio porte (~100 a 1000 páginas) — processos em trâmite ordinário com volume razoável de peças, provas e decisões. Utiliza estratégia de leitura faseada com indexação de peças e síntese hierárquica, preservando profundidade analítica. Use para processos cíveis, trabalhistas, tributários ou administrativos em fase avançada com acervo documental substancial.
---

# /analise-processo-medio — Análise de Processo Médio (~100 a 1000 páginas)

> Consulte [CONNECTORS.md](../../CONNECTORS.md).

Análise de autos processuais ou administrativos com volume intermediário — tipicamente processos em rito comum, com fase instrutória parcial ou integral concluída, múltiplas petições, decisões interlocutórias, laudos periciais e recursos. A estratégia é **leitura faseada** (sem perda de profundidade) com **indexação** da peça documental.

**Vedação à alucinação — inegociável.** Mesmas regras da análise pequena: **somente** o que consta dos autos ou de direito positivo objetivo; inferências rotuladas; lacunas reportadas.

## Invocação

```
/analise-processo-medio [arquivo / URL / nº CNJ]
```

## Estratégia de análise (faseada, mas integral)

### Fase 0 — Preparação

1. Identificar o **total de páginas** e a estrutura dos autos (principal, anexos, cadernos separados, apensos).
2. Confirmar com o usuário:
   - Objetivo da análise (peça a elaborar, prazo, foco)
   - Se há **áreas de foco** que permitam priorizar a leitura (mérito vs. processual; prescrição; prova pericial; matéria específica)
   - Se a casa já possui **índice dos autos** ou histórico processual consolidado
3. Preparar plano de leitura estruturado.

### Fase 1 — Indexação macroestrutural

Varrer os autos para construir **índice cronológico/topológico**:

| ID | Data | Peça | Parte | Fls./ID | Natureza |
|----|------|------|-------|---------|----------|
| 01 | [data] | Petição inicial | [autor] | 1-25 | peça inaugural |
| 02 | [data] | Procuração e documentos | [autor] | 26-40 | documentos |
| 03 | [data] | Decisão de recebimento | — | 41 | decisão |
| 04 | [data] | Contestação | [réu] | 42-80 | peça |
| 05 | [data] | Réplica | [autor] | 81-95 | peça |
| 06 | [data] | Saneador | — | 96 | decisão interlocutória |
| 07 | [data] | Laudo pericial | perito | 97-200 | prova |
| ... | | | | | |

O índice é o **mapa** de navegação — permitirá referências precisas e evitará releituras.

### Fase 2 — Leitura dirigida por camadas

**Camada 1 — Peças centrais** (leitura integral):
- Petição inicial + emenda(s)
- Contestação + reconvenção (se houver)
- Réplica
- Saneador / decisão organizadora do processo (art. 357 CPC)
- Sentença de 1º grau e acórdãos (se houver)
- Recurso(s) e contrarrazões em curso
- Decisões interlocutórias relevantes (de mérito parcial, tutelas, nulidades)

**Camada 2 — Provas determinantes**:
- Laudos periciais e esclarecimentos
- Atas de audiência / depoimentos (transcritos ou gravados — se disponível transcrição)
- Documentos de valor probatório crucial (contratos, notas fiscais, e-mails, laudos técnicos)

**Camada 3 — Movimentações e manifestações acessórias**:
- Despachos, petições de mero expediente, juntadas, publicações — lidas para confirmar **cronologia, prazos e ausências**

Cada camada é lida **integralmente no seu escopo**. Não se faz "amostragem". A camada 3 pode ser lida em paralelo, em regime de varredura, para confirmar o controle cronológico e de prazos.

### Fase 3 — Extração estruturada

Durante a leitura, catalogar de forma estruturada:

- **Teses das partes** (com citação literal da fundamentação, fls.)
- **Evolução processual** (o que cada decisão consolidou ou afastou)
- **Matriz probatória** — o que está provado, o que está controvertido, o que é ônus de cada parte (art. 373 CPC; art. 6º, VIII, CDC para inversão)
- **Questões preliminares e prejudiciais**
- **Prescrição / decadência**
- **Nulidades** (absolutas e relativas — art. 276-283 CPC)

### Fase 4 — Análise técnica integral

Só depois de Fase 0-3 completas, produzir a análise. Isso evita o vício comum de analisar com base em resumo prematuro e incompleto.

## Formato de saída

```
## Análise Processual — [Natureza / Nº CNJ]
**Parte representada**: [—]
**Objetivo**: [—]
**Volume analisado**: [x páginas em y peças]
**Tempo de análise**: [—]
**Data**: [—]

### 1. Identificação
- **Número CNJ**: [—]
- **Órgão**: [Vara / Turma / Seção]
- **Juízo**: [—]
- **Rito**: [—]
- **Partes**: [qualificação]
- **Representação da casa**: [advogado, OAB/UF]
- **Fase atual**: [—]
- **Última movimentação**: [—]
- **Valor da causa**: [R$] (atualizado em [data])

### 2. Índice da peça documental
[Tabela com peças, datas, fls./ID — sumário macroestrutural]

### 3. Síntese factual (reconstrução cronológica)
[Prosa densa com referência a fls./ID; distinção clara entre fatos incontroversos, controvertidos e pendentes de prova]

### 4. Teses e fundamentação
#### 4.1 Parte [autora]
[Teses principais, dispositivos invocados, provas apresentadas, evolução nas peças — com fls.]

#### 4.2 Parte [ré]
[Idem]

#### 4.3 Teses eventualmente apresentadas por terceiros
[Amicus, assistente, denunciado à lide, MP]

### 5. Evolução processual (linha do tempo)
| Data | Evento | Impacto |
|------|--------|---------|
| [—] | Saneador | fixou as seguintes questões de fato/direito; distribuiu o ônus da prova nos termos do art. 373 CPC |
| [—] | Laudo pericial | concluiu pela [—] |
| [—] | Sentença de 1º grau | [acolheu/rejeitou] pedidos [—] |
| [—] | Apelação | preliminares e razões |

### 6. Matriz probatória
| Fato | Controvertido? | Ônus | Prova produzida | Avaliação |
|------|---------------|------|-----------------|-----------|
| [—] | sim | autor (art. 373, I CPC) | [laudo pericial fls. X] | suficiente / insuficiente |

### 7. Decisões relevantes — análise
[Para cada decisão central — fundamentação, impacto, pontos a atacar/sustentar em sede recursal]

### 8. Análise técnica pela casa
[Por tese — avaliação da robustez; fragilidades próprias; oportunidades argumentativas; fragilidades da contraparte; nulidades identificadas; divergência doutrinária/jurisprudencial **somente se identificada**]

### 9. Inconsistências e pontos críticos
[Lista — com fls. precisas]

### 10. Prescrição / decadência / nulidades
[Avaliação específica com dispositivos]

### 11. Prazos em curso e pendências
[—]

### 12. Recomendação estratégica
[Próxima peça; estratégia recursal; sugestões probatórias; viabilidade de acordo]

### 13. Minuta preliminar (se solicitado)
[Esqueleto estruturado da peça — com [A PREENCHER] para dados não constantes]

### 14. Lacunas
[Documentos referenciados e não localizados; peças não juntadas; dados incompletos]
```

## Observações

- **Sem sumarização prematura.** A estratégia faseada preserva profundidade: cada camada é lida em seu escopo antes de qualquer síntese.
- **Referência precisa** a fl./ID em cada afirmação factual. O advogado deve poder conferir rapidamente.
- **Divergência doutrinária/jurisprudencial** é mencionada **apenas se** identificada nas fontes. Recomendar pesquisa dedicada em STJ/STF/TST quando pertinente.
- Para processos que requeiram múltiplas sessões de análise, a IA preserva o estado (índice + anotações) entre as sessões.
- **Linguagem técnica, formal, em PT-BR culto.**
- Se o volume ultrapassar ~1000 páginas, **migrar para `/analise-processo-extenso`**.
