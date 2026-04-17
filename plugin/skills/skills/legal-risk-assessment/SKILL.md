---
name: legal-risk-assessment
description: Classifica riscos jurídicos segundo matriz de severidade × probabilidade, com critérios de escalonamento. Alinha-se ao CPC 25 (provável / possível / remoto) para efeito de provisão contábil e reporte em notas explicativas. Use para avaliar exposição em contratos, litígios em curso, contingências societárias, decisões de negócio com implicações regulatórias e classificação para fins de reporte.
argument-hint: "<caso / contrato / contingência>"
---

# /avaliar-risco — Avaliação de Risco Jurídico

> Consulte [CONNECTORS.md](../../CONNECTORS.md).

Classifica risco jurídico com base em **severidade × probabilidade**, compatível com o CPC 25 para efeitos contábeis, e define o encaminhamento interno.

**Vedação à alucinação.** A probabilidade **jamais** é atribuída por intuição. Deriva de: (i) documentação do caso; (ii) pareceres internos anteriores; (iii) jurisprudência efetivamente identificada em fonte conectada ou aportada pelo usuário; (iv) manifestações de autoridade quando existentes. Inexistindo base, a IA declara "classificação preliminar — exige aprofundamento".

## Invocação

```
/avaliar-risco [caso / contrato / contingência]
```

## Estrutura de avaliação

### Dimensão 1 — Severidade

Mensura o **impacto** caso o risco se materialize. Critérios:

| Nível | Critério |
|-------|----------|
| **Crítico** | Impacto financeiro > [alçada crítica do escritório/cliente]; risco criminal a pessoa física; ingresso em lista restritiva (CEIS, CNEP, OFAC); perda de licença/autorização; comprometimento reputacional grave; paralisação de atividade-fim |
| **Alto** | Impacto financeiro significativo; sanção administrativa relevante (ANPD, CVM, BACEN, CADE); litígio de massa; comprometimento reputacional setorial |
| **Médio** | Impacto financeiro moderado; sanção administrativa contornável; litígio individual de valor relevante; desconformidade regulatória corrigível |
| **Baixo** | Impacto financeiro marginal; risco de discussão contratual; litígio individual de baixo valor |

### Dimensão 2 — Probabilidade (CPC 25 alinhado)

| Nível | Critério | CPC 25 |
|-------|----------|--------|
| **Muito alta** | Fatos incontroversos + jurisprudência dominante desfavorável + decisão desfavorável já proferida | Provável (> 50%) |
| **Alta** | Fatos provados + jurisprudência majoritária desfavorável | Provável |
| **Média** | Fatos controversos + jurisprudência dividida | Possível |
| **Baixa** | Fatos defensáveis + jurisprudência majoritária favorável | Possível |
| **Muito baixa** | Fatos inexistentes ou claramente favoráveis + jurisprudência pacífica favorável | Remoto |

### Matriz severidade × probabilidade

| | **Muito baixa** | **Baixa** | **Média** | **Alta** | **Muito alta** |
|---|---|---|---|---|---|
| **Crítico** | M | A | A | C | C |
| **Alto** | B | M | A | A | C |
| **Médio** | B | B | M | A | A |
| **Baixo** | B | B | B | M | M |

Legenda: **B** = baixo — acompanhamento; **M** = médio — mitigação; **A** = alto — ação corretiva imediata; **C** = crítico — escalonamento à alta direção e eventual provisão/reporte regulatório.

## Fluxo

### Fase 1 — Coleta factual

- **Descrição do caso** (contrato / litígio / contingência)
- **Partes envolvidas**
- **Valor em discussão**
- **Documentos disponíveis** (contrato, peças processuais, comunicações, pareceres anteriores, atas)
- **Estágio processual / regulatório / negocial**
- **Histórico** — pedidos/condenações similares

### Fase 2 — Análise das dimensões

#### Severidade
- Dimensionar o impacto financeiro (valor do pedido, multa aplicável, efeito em operações, perda de licença)
- Avaliar impacto criminal (Lei 8.137/90 — crimes tributários; Lei 7.492/86 — crimes contra o SFN; Lei 12.846/2013 — corrupção empresarial; CP — estelionato, apropriação indébita, lavagem — Lei 9.613/98)
- Avaliar impacto reputacional
- Avaliar impacto operacional (paralisação, impedimento licitatório)

#### Probabilidade
- Avaliar os fatos — incontroversos? controvertidos? favoráveis?
- Avaliar o direito aplicável — jurisprudência **efetivamente** identificada (sem inventar); súmulas e temas repetitivos em STF/STJ/TST quando localizados
- Avaliar a **chance de êxito** na defesa/acusação (quando cabível opinião técnica fundamentada)

### Fase 3 — Recomendação e encaminhamento

- **Classificação** (B/M/A/C)
- **Ações mitigatórias** sugeridas
- **Responsável** pelo acompanhamento
- **Cadência de revisão** (mensal, trimestral, conforme a matéria)
- **Provisão contábil** sugerida (se aplicável — CPC 25)
- **Reporte regulatório** exigível (CVM Res. 44 — fato relevante; ANPD — incidente; comunicação a autoridades conforme setor)

## Formato de saída

```
## Avaliação de Risco — [caso]

### 1. Síntese do caso
[—]

### 2. Dimensões
- **Severidade**: [nível] — [justificativa]
- **Probabilidade**: [nível] — [justificativa com base em documentos/precedentes efetivamente localizados]

### 3. Classificação
**[B / M / A / C]**
Equivalente CPC 25: **[provável / possível / remoto]**

### 4. Fundamentação
[Prosa técnica com citação precisa de documentos, dispositivos aplicáveis e precedentes identificados — sem citações inventadas]

### 5. Impacto potencial
- Financeiro: R$ [—] ([metodologia])
- Criminal: [—]
- Regulatório: [—]
- Reputacional: [—]
- Operacional: [—]

### 6. Recomendação
- **Ação imediata**: [—]
- **Mitigação**: [—]
- **Responsável**: [—]
- **Cadência de revisão**: [—]

### 7. Provisão contábil sugerida (se aplicável)
- Valor: R$ [—]
- Base CPC 25: [—]

### 8. Reporte regulatório / societário
- Fato relevante CVM (Res. 44/2021): [sim / não / avaliar]
- Comunicação LGPD à ANPD / titulares: [sim / não / avaliar]
- Comunicação setorial (BACEN / CADE / ANS / outros): [sim / não / avaliar]

### 9. Lacunas para aprofundamento
[Pesquisa jurisprudencial dedicada recomendada; documentos não localizados; pareceres a obter]
```

## Observações

- **Revisão do responsável técnico** sempre exigida antes de qualquer reporte externo (contábil, societário, regulatório).
- **Jamais inventar** precedente, percentual de êxito ou posição de autoridade.
- **Classificação preliminar** é explicitada como tal quando não houver base documental suficiente.
- **Sigilo** preservado em toda a produção — matéria submetida a sigilo profissional.
- **Linguagem técnica, formal, PT-BR culto.**
