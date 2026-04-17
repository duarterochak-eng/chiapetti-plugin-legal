---
name: analise-processo-pequeno
description: Analisa processos judiciais ou administrativos de pequeno porte (até ~100 páginas) — peças isoladas, JEC, processos iniciais ou análise pontual de petição, decisão ou laudo específico. Realiza leitura integral com síntese estruturada, identifica teses, fundamentos legais, pontos críticos e inconsistências. Use para qualquer processo até 100 páginas ou análise focada em peça individual.
---

# /analise-processo-pequeno — Análise de Processo Pequeno (até ~100 páginas)

> Consulte [CONNECTORS.md](../../CONNECTORS.md).

Análise de autos processuais ou administrativos de pequeno porte — processos em Juizado Especial Cível (Lei 9.099/95), demandas iniciais, peças isoladas (petição, contestação, decisão, laudo) ou recortes pontuais. A estratégia é **leitura integral** dos autos, com síntese estruturada e análise técnica.

**Vedação à alucinação — inegociável.** A IA analisa **somente** o que consta dos autos ou de direito positivo objetivo (dispositivos legais, normas vigentes). Não presume jurisprudência, doutrina ou fatos não comprovados. Inferências próprias são rotuladas como "análise do signatário". Lacunas são expressamente reportadas.

## Invocação

```
/analise-processo-pequeno [arquivo / URL / nº CNJ / texto]
```

## Fluxo

### Fase 0 — Briefing

Confirmar com o usuário:
- **Objetivo da análise** (peça a elaborar, parecer, verificação de viabilidade, contra-arrazoado, recurso)
- **Prazo** (se houver)
- **Parte representada** pela casa
- **Foco específico** — se análise de peça isolada, indicar qual

### Fase 1 — Leitura integral

Leitura completa do material. Em processos de até 100 páginas não há fracionamento: todo o conteúdo é processado integralmente. Durante a leitura, capturar:

- Teses das partes (com fls./ID e citação literal quando crítica)
- Pedidos e fundamentação
- Provas apresentadas
- Decisões proferidas
- Prazos em curso
- Dispositivos legais efetivamente invocados

### Fase 2 — Extração estruturada

- **Fatos** — incontroversos vs. controvertidos
- **Fundamentos jurídicos** invocados por cada parte
- **Ônus probatório** (art. 373 CPC; art. 6º, VIII CDC para inversão nas relações consumeristas)
- **Preliminares e prejudiciais** (incompetência, litispendência, prescrição, decadência, carência de ação)
- **Nulidades** (art. 276-283 CPC)

### Fase 3 — Análise técnica

Avaliação de mérito pela casa — robustez das teses próprias, fragilidades, oportunidades argumentativas, fragilidades da contraparte. Identificação de divergência doutrinária ou jurisprudencial **apenas** se efetivamente constante nos autos ou em fonte conectada verificável.

## Formato de saída

```
## Análise Processual — [Natureza / Nº CNJ ou identificador]
**Parte representada**: [—]
**Objetivo**: [—]
**Volume**: [x páginas]
**Data**: [—]

### 1. Identificação
- **Número CNJ / processo administrativo**: [—]
- **Órgão**: [Vara / Juizado / Autoridade]
- **Rito**: [comum / sumaríssimo (JEC) / trabalhista / administrativo]
- **Partes**: [qualificação]
- **Representação da casa**: [advogado, OAB/UF]
- **Fase atual**: [—]
- **Valor da causa**: [R$] (atualizado em [data])

### 2. Síntese factual
[Prosa densa com referência a fls./ID; distinção entre fatos incontroversos, controvertidos e pendentes de prova]

### 3. Teses e fundamentação
#### 3.1 Parte [autora]
[Teses, dispositivos invocados, provas apresentadas — com fls.]

#### 3.2 Parte [ré]
[Idem]

### 4. Decisões proferidas
[Síntese de cada decisão — fundamentação e impacto]

### 5. Análise técnica pela casa
[Robustez das teses, fragilidades próprias, oportunidades, fragilidades da contraparte; divergência doutrinária/jurisprudencial somente se identificada nas fontes]

### 6. Preliminares, prejudiciais e nulidades
[Prescrição, decadência, incompetência, carência, nulidades — com dispositivos]

### 7. Matriz probatória
| Fato | Controvertido? | Ônus | Prova produzida | Avaliação |
|------|---------------|------|-----------------|-----------|
| [—] | sim | autor (art. 373, I CPC) | [—] | suficiente / insuficiente |

### 8. Inconsistências e pontos críticos
[Lista — com fls. precisas]

### 9. Prazos em curso
[—]

### 10. Recomendação estratégica
[Próxima peça, sugestões probatórias, viabilidade de acordo, risco de sucumbência]

### 11. Minuta preliminar (se solicitado)
[Esqueleto da peça com campos [A PREENCHER] para dados não constantes]

### 12. Lacunas
[Documentos referenciados e não localizados; dados incompletos]
```

## Observações

- **Referência precisa** a fl./ID em cada afirmação factual.
- **Divergência doutrinária/jurisprudencial** mencionada **apenas** se identificada nas fontes — jamais inventada.
- **Linguagem técnica, formal, em PT-BR culto.** Terminologia jurídica precisa.
- Se o volume ultrapassar ~100 páginas, **migrar para `/analise-processo-medio`**.
