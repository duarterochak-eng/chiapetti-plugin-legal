---
name: analise-processo-extenso
description: Analisa processos judiciais ou administrativos extensos (1000+ páginas) — processos de massa, recuperações judiciais, ações coletivas, autos robustos de M&A contencioso, processos tributários com grande volume, procedimentos de compliance com acervo documental extenso. Utiliza estratégia de chunking hierárquico, indexação minuciosa e sumarização em múltiplas camadas, preservando rigor técnico e rastreabilidade integral. Use para qualquer processo que exceda 1000 páginas ou que envolva múltiplos apensos, cadernos ou anexos extensos.
---

# /analise-processo-extenso — Análise de Processo Extenso (1000+ páginas)

> Consulte [CONNECTORS.md](../../CONNECTORS.md).

Análise de autos processuais de grande volume — acima de 1000 páginas, frequentemente com múltiplos apensos, cadernos e anexos, tipicamente em recuperações judiciais (Lei 11.101/2005), ações civis públicas, ações coletivas (Lei 8.078/90, Lei 7.347/85), processos tributários volumosos, litígios societários e arbitragens complexas. Utiliza **estratégia de chunking hierárquico** com indexação minuciosa e síntese em múltiplas camadas.

**Vedação à alucinação — absoluta e auditável.** Dada a dimensão, o risco de extrapolação é maior. A IA adota protocolo rigoroso:

- Cada afirmação factual é **rastreável** à fl./ID exata
- Citações de dispositivos só quando efetivamente invocados nos autos ou quando de direito positivo objetivo
- **Jamais** inventa jurisprudência, doutrina, súmula, enunciado ou precedente
- Inferências próprias são **rotuladas** como "análise do signatário"
- Lacunas (peças ausentes, documentos referenciados e não juntados) são reportadas
- Quando o volume exigir sumarização, a IA **preserva links rastreáveis** a cada peça e, quando requisitada, reabre o conteúdo literal

## Invocação

```
/analise-processo-extenso [arquivo / URL / pasta / nº CNJ]
```

Aceita: upload de múltiplos PDFs, URL para pasta em ~~armazenamento, ou nº CNJ com acesso a PJe/e-SAJ/Projudi configurado.

## Estratégia em 6 fases

### Fase 0 — Briefing e escopo

Perguntar ao usuário:
- **Objetivo** (peça a elaborar, parecer, defesa, sustentação, contra-arrazoado, embargos, agravo, ACP, RE/REsp)
- **Prazo** disponível e fases a priorizar
- **Foco temático** (matéria/tese a aprofundar) — se houver; se não, leitura integral fatiada
- **Apensos e cadernos** (há? quais? estão disponíveis?)
- **Histórico interno** — a casa já possui memoriais, fichas, minutas anteriores que possam servir de base
- **Nível de rastreabilidade** requerido (para uso interno vs. para peça com citação literal em juízo)

### Fase 1 — Mapeamento estrutural e inventário

Antes de qualquer leitura analítica:

1. **Inventariar** todos os arquivos (processo principal, apensos, cadernos, anexos)
2. **Normalizar nomenclatura** (arquivo X = "volume 3 da instrução" = fls. 1.200 a 1.450 dos autos)
3. **Identificar volumetria**: total de páginas, número de peças, tipos de documento (peças processuais, contratos, notas, laudos, depoimentos, correspondências, publicações)
4. **Mapear** apensos e sua relação com o principal
5. **Criar índice-mestre** — tabela topológica e cronológica consolidando todas as peças

O índice-mestre é o artefato crítico: serve de mapa e de âncora de rastreabilidade.

### Fase 2 — Chunking hierárquico

Dividir o material em blocos lógicos **hierárquicos**:

- **Nível 1 — Blocos macro**: (a) peças inaugurais e defesa; (b) instrução probatória documental; (c) perícias; (d) audiências e depoimentos; (e) decisões e recursos; (f) incidentes (cumprimento provisório, tutela, etc.); (g) apensos específicos
- **Nível 2 — Sub-blocos** dentro de cada macro: petição inicial + emenda; cada laudo; cada decisão; cada recurso
- **Nível 3 — Unidades analíticas** individuais: peça/decisão/laudo específico

O chunking é **lógico**, não puramente por página. Uma petição inicial de 200 páginas é uma unidade; 800 páginas de documentos anexos podem ser múltiplas unidades conforme temática.

### Fase 3 — Leitura e sumarização em duas passadas

**Passada 1 — Extração bruta por unidade:**

Para cada unidade analítica:
- Capturar, **com citação literal e referência precisa**, as teses, pedidos, fundamentos, provas, decisões
- Registrar: data, autor, fls., dispositivos invocados, conclusões
- **Não sintetizar ainda** — apenas extrair

**Passada 2 — Sumarização hierárquica:**

- Síntese por **unidade** (ex.: resumo do laudo pericial — 3-5 períodos com referência a páginas)
- Síntese por **sub-bloco** (ex.: toda a fase instrutória pericial — 10-15 períodos)
- Síntese por **bloco macro** (ex.: toda a fase de defesa — 20-30 períodos)
- Síntese **integral** do processo (1-2 páginas densas)

A síntese integral é **derivada** das camadas inferiores. Cada afirmação remete a uma fonte verificável.

### Fase 4 — Análise técnica por eixo

Paralelamente, consolidar por **eixos analíticos**:

1. **Eixo factual** — o que está provado / controvertido / ainda pendente de prova
2. **Eixo jurídico** — teses, dispositivos, correntes identificadas
3. **Eixo processual** — preliminares, prejudiciais, nulidades, prescrição, competência, legitimidade
4. **Eixo probatório** — matriz de provas, ônus (art. 373 CPC; art. 6º, VIII CDC), ainda a produzir
5. **Eixo recursal** — decisões impugnáveis e cabíveis
6. **Eixo temporal** — prazos, decadência, prescrição, andamento

Cada eixo referencia as unidades analíticas subjacentes — o advogado pode descer do geral ao literal quando precisar.

### Fase 5 — Recomendação e produção

Somente após Fases 0-4, formular:
- Recomendação estratégica
- Minuta preliminar da peça-alvo (se solicitada)
- Matriz de riscos (chamar `/avaliar-risco` quando pertinente)
- Pontos que exigem pesquisa jurisprudencial dedicada (recomendar ao usuário — **não inventar**)

## Formato de saída

### Relatório principal

```
## Análise Processual Extensa — [Natureza / Nº CNJ]
**Parte representada**: [—]
**Objetivo**: [—]
**Volume analisado**: [x páginas] em [y peças] em [z arquivos/cadernos]
**Apensos**: [—]
**Data**: [—]

### 1. Identificação
- **Número CNJ**: [—]
- **Órgão**: [—]
- **Juízo / Relator**: [—]
- **Rito**: [—]
- **Partes**: [qualificação condensada; relação anexa para múltiplas partes]
- **Procuradores da casa**: [—]
- **Fase atual**: [—]
- **Última movimentação**: [—]
- **Valor da causa**: [R$] (atualizado em [data])
- **Natureza da demanda**: [—]

### 2. Sumário executivo
[1-2 páginas densas: do que se trata, teses centrais, estado processual, principais riscos, recomendação final. Escrita em prosa formal, sem repetições.]

### 3. Índice-mestre dos autos
[Tabela com todos os blocos macro, sub-blocos e unidades analíticas — com datas, fls./ID, autores, natureza. Este é o mapa.]

### 4. Síntese factual (em camadas)
#### 4.1 Visão integral
[Prosa consolidada — 20-30 períodos densos]

#### 4.2 Por fase
- **Pré-processual**: [—]
- **Inicial**: [—]
- **Resposta**: [—]
- **Instrutória**: [—]
- **Decisória**: [—]
- **Recursal**: [—]
- **Cumprimento / incidentes**: [—]

### 5. Teses das partes (condensadas, com referência)
#### 5.1 Parte [autora/exequente]
[Teses ao longo do processo, evolução nas peças, com fls. exatas]

#### 5.2 Parte [ré/executada]
[Idem]

#### 5.3 Terceiros (se aplicável)
[Litisconsortes, assistentes, amicus, MP, denunciados à lide]

### 6. Decisões centrais — análise
[Para cada decisão relevante (saneador, sentença, acórdão, decisões interlocutórias de peso): síntese, fundamentação, impacto, pontos de ataque/sustentação recursal — com citação literal quando crítica]

### 7. Matriz probatória
[Tabela consolidada: fato × prova × ônus × suficiência]

### 8. Análise técnica por eixo
- **Preliminares e prejudiciais**: [—]
- **Mérito — tese 1 / tese 2 / tese N**: [—]
- **Nulidades identificadas**: [—]
- **Prescrição / decadência**: [—]
- **Competência e legitimidade**: [—]
- **LGPD / sigilo / proteção de dados processuais**: [—] (art. 189 CPC; LGPD)

### 9. Inconsistências, lacunas documentais e pontos críticos
[Lista objetiva — com fls.]

### 10. Riscos e exposição
[Chama `/avaliar-risco` quando pertinente; resumo da classificação, provisionamento sugerido, impactos]

### 11. Pendências, prazos e diligências
[—]

### 12. Recomendação estratégica
[Próxima peça, estratégia recursal, prova pendente, recomendações de compliance/negocial/transacional]

### 13. Minuta preliminar (se solicitado)
[Esqueleto da peça, com campos [A PREENCHER]]

### 14. Lacunas de informação
[Documentos referenciados e não localizados; peças citadas nos autos mas ausentes; dados incompletos]

### 15. Índice remissivo
[Para consulta rápida — principais temas → fls.]
```

### Artefatos complementares recomendados

- **Índice-mestre** — arquivo próprio (.xlsx ou .md) com a tabela consolidada
- **Ficha-resumo por peça** — arquivo por peça central
- **Cronologia visual** (linha do tempo) — opcional
- **Matriz de teses** (.xlsx) — tese × peça × fundamentação × prova × status

## Observações críticas

- **Preservar rastreabilidade integral.** Cada afirmação, síntese ou conclusão remete a uma unidade analítica e, desta, a fls. específicas. Sem isso, a análise perde valor em juízo.
- **Trabalho iterativo.** Processos dessa magnitude frequentemente exigem múltiplas sessões. A IA preserva o índice-mestre, as fichas e a matriz entre sessões, servindo como base consolidada para o trabalho da casa.
- **Não tentar "ler tudo de uma vez".** O chunking hierárquico existe justamente para permitir profundidade sem perda de qualidade.
- **Jurisprudência / doutrina externa** — recomendar pesquisa dedicada quando pertinente ao caso. Jamais inventar.
- **Sigilo.** Processos volumosos frequentemente correm sob sigilo (art. 189 CPC, LGPD, segredo empresarial, Lei 9.279/96 art. 206). Os artefatos produzidos devem preservar o sigilo e ser marcados como **"Matéria submetida a sigilo profissional — uso interno"**.
- **Linguagem técnica, formal, em PT-BR culto.** Nenhuma informalidade. Terminologia jurídica precisa.
- Quando a análise exigir uso de ferramentas adicionais (extração de texto de PDF, OCR, indexação textual), a IA utiliza a skill `pdf` e `xlsx` como suporte, mantendo a padronização.
- Em recuperações judiciais, atentar para: prazos do art. 6º Lei 11.101/2005, assembleia de credores (arts. 35-46), plano (arts. 53-55), quórum, cram-down (art. 58), observação de subclasses, habilitação (arts. 7º-20), impugnações; possível conflito entre plano homologado e execuções fiscais (arts. 6º, 73 e 187 CTN).
- Em ações coletivas, atentar para: legitimidade (art. 5º Lei 7.347/85; art. 82 CDC), coisa julgada coletiva (art. 103 CDC), liquidação individual (art. 97 CDC).
