---
name: triage-nda
description: Triagem rápida de NDA (Acordo de Confidencialidade) recebido, classificando-o como VERDE (aprovação-padrão), AMARELO (revisão por advogado) ou VERMELHO (revisão completa). Use quando chegar NDA de prospect, parceiro, fornecedor ou cliente; ao rastrear non-solicits, non-competes, cláusulas sem carve-outs, prazos abusivos, penalidades desproporcionais; ao decidir se o NDA pode ser assinado sob alçada delegada. Ancorado no CC/2002 (arts. 421-422), Lei 9.279/96 (art. 195 — concorrência desleal) e LGPD quando envolver dados pessoais.
argument-hint: "<arquivo ou texto de NDA>"
---

# /triar-nda — Triagem de NDA

> Consulte [CONNECTORS.md](../../CONNECTORS.md).

Classifica NDA recebido em três faixas — **VERDE** (aceitável, aprovação delegada), **AMARELO** (revisão por advogado antes de assinar), **VERMELHO** (revisão completa ou negociação) — conforme critérios objetivos.

**Vedação à alucinação.** A triagem baseia-se **apenas** no texto recebido, confrontado com o playbook local. Nenhuma interpretação de jurisprudência não identificada. Inferências rotuladas.

## Invocação

```
/triar-nda [arquivo / texto]
```

## Critérios de triagem

### Identificação inicial
- **Partes** (razão social, CNPJ, endereço)
- **Mutualidade** — mútuo (preferido) vs. unilateral (aceitável em contextos específicos, como contratação de prestador)
- **Objeto** da relação (escopo da finalidade da troca de informações)
- **Prazo** (vigência do NDA e do dever de sigilo)
- **Lei aplicável** e foro/arbitragem
- **Definição de "Informação Confidencial"**
- **Carve-outs** (exceções)
- **Penalidades**

### VERDE — Aprovação delegada (assinar com revisão sumária)

Todos os critérios simultaneamente satisfeitos:

- Mútuo (ou unilateral em contexto coerente com a casa recebendo informação)
- Prazo de sigilo ≤ 5 anos (ou indeterminado para segredo de indústria — art. 195 Lei 9.279/96)
- Definição ampla mas razoável de "Informação Confidencial" (admite-se "informações marcadas como confidenciais ou que razoavelmente se apresentem como tal")
- Carve-outs completos:
  - (a) informação pública ou que se torne pública sem violação ao NDA
  - (b) informação já conhecida antes da divulgação
  - (c) informação desenvolvida independentemente
  - (d) informação recebida legitimamente de terceiro sem dever de confidencialidade
  - (e) informação exigida por lei, ordem judicial ou autoridade competente (com dever de comunicação à parte divulgadora e limitação à informação estritamente necessária)
- Ausência de cláusula de non-solicit, non-compete ou exclusividade
- Foro brasileiro (comarca da sede de uma das partes) e lei brasileira; OU arbitragem em câmara reconhecida (CAM-CCBC, CAMARB, CCI) com sede no Brasil e idioma português
- Devolução/destruição de informação ao término, com período de retenção razoável para fins regulatórios e de backup
- LGPD mencionada quando houver troca de dados pessoais, com DPA anexo ou disposições mínimas (art. 46 LGPD — medidas de segurança; art. 48 — comunicação de incidente)
- Penalidade proporcional (multa contratual em valor razoável; tutela específica cabível)

### AMARELO — Revisão por advogado antes de assinar

Qualquer uma das hipóteses:

- Prazo de 5 a 10 anos (exceto segredo de indústria)
- Definição genérica excessiva (ex.: "toda informação compartilhada"), sem possibilidade de marcação; sem exclusões
- Carve-outs incompletos (falta um ou mais dos itens a-e)
- Mutualidade parcial (obrigações desproporcionais)
- Ausência de dispositivos LGPD quando há troca de dados pessoais
- Foro de eleição em comarca estranha a ambas as partes
- Arbitragem em câmara não reconhecida ou em idioma estrangeiro (contratos domésticos)
- Cláusula de auditoria desproporcional
- Obrigação de devolução sem janela de retenção para backup/obrigação legal

### VERMELHO — Revisão completa ou negociação

Qualquer uma das hipóteses:

- Prazo superior a 10 anos (exceto segredo de indústria)
- Cláusula de **non-solicit** (não aliciamento de funcionários/clientes) — fere livre iniciativa e livre exercício profissional (art. 5º, XIII CF; art. 170 CF); admitida apenas em contexto de M&A específico
- Cláusula de **non-compete** (não concorrência) — em NDA é sinal vermelho; admite-se em contrato específico, com contrapartida pecuniária, escopo territorial e temporal razoáveis, no contexto do art. 170 CF e arts. 424 e 473 CC
- Penalidade desproporcional (multa manifestamente excessiva — art. 413 CC permite redução judicial; sinal de negociação abusiva)
- Exclusividade disfarçada
- Transferência de dados pessoais internacional sem base legal (arts. 33-36 LGPD)
- Renúncia antecipada a direitos (art. 424 CC em adesão)
- Foro estrangeiro em contrato doméstico sem fundamento
- Cessão a qualquer momento pela contraparte sem anuência
- Responsabilidade sem limite em contexto comercial
- Ausência total de LGPD em transferência relevante de dados pessoais
- Contraparte é entidade governamental / autoridade regulatória (exige modelo próprio); contraparte em lista restritiva (CEIS, CNEP, OFAC); contraparte com restrições setoriais específicas (saúde, financeiro)

## Fluxo

### Fase 1 — Extração estruturada

Da minuta recebida, extrair:

- Partes e suas qualificações
- Mutualidade
- Definição de Informação Confidencial
- Carve-outs
- Prazo
- Obrigações (devolução, comunicação de incidente, uso)
- Penalidades
- Foro/lei/arbitragem
- Cláusulas atípicas (non-solicit, non-compete, exclusividade, auditoria)
- Cláusulas LGPD

### Fase 2 — Confronto com playbook

Comparar contra o playbook local (`legal.local.md` — padrões do escritório).

### Fase 3 — Classificação e saída

Emitir a classificação (VERDE / AMARELO / VERMELHO) e, para AMARELO e VERMELHO, as sugestões de ajuste.

## Formato de saída

```
## Triagem de NDA — [contraparte]
**Classificação**: [🟢 VERDE / 🟡 AMARELO / 🔴 VERMELHO]
**Data**: [—]

### 1. Síntese
- **Partes**: [—]
- **Mutualidade**: [—]
- **Prazo**: [—]
- **Foro / lei**: [—]
- **LGPD**: [—]

### 2. Checklist de critérios
| Item | Status | Observação |
|------|--------|------------|
| Mutualidade | ✓ / ✗ | [—] |
| Prazo razoável | | |
| Definição de Informação Confidencial | | |
| Carve-outs completos | | |
| LGPD endereçada | | |
| Foro/lei apropriados | | |
| Ausência de non-solicit/non-compete | | |
| Penalidade proporcional | | |

### 3. Pontos de atenção (se AMARELO / VERMELHO)
[Desvios específicos com fundamentação]

### 4. Sugestões de ajuste
[Redação alternativa proposta, cláusula a cláusula]

### 5. Encaminhamento
- **VERDE**: aprovar assinatura sob alçada delegada → `/solicitar-assinatura`
- **AMARELO**: revisão por advogado responsável → anotar em `~~gestão`
- **VERMELHO**: revisão completa / negociação → acionar `/revisar-contrato`

### 6. Lacunas
[Informações adicionais requeridas]
```

## Observações

- **Non-compete** em NDA é sinal forte de negociação abusiva. Non-competes valem como cláusula autônoma com contrapartida pecuniária, escopo limitado e proporcionalidade (há divergência doutrinária; há precedentes do TST sobre limitação de até 2 anos e contrapartida salarial — mencionar apenas se identificada fonte).
- **Segredo de indústria** — art. 195 Lei 9.279/96 protege ad eternum; prazo indeterminado é aceitável apenas para essa hipótese.
- **LGPD** — quando houver troca de dados pessoais, o NDA **deve** conter disposições mínimas ou remeter a DPA.
- **Revisão humana** obrigatória antes de assinatura em qualquer classificação.
- **Linguagem técnica, formal, PT-BR culto.**
