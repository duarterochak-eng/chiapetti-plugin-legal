---
name: vendor-check
description: Verifica status de acordos existentes com um fornecedor/cliente/parceiro em todos os sistemas conectados — CLM, CRM, e-mail, armazenamento — com análise de lacunas e prazos próximos. Inclui checagens de compliance brasileiras típicas (CND Federal/Estadual/Municipal, SICAF, CNDT, CEIS, CNEP, OFAC/sanções, certidão negativa trabalhista). Use ao homologar novo fornecedor, renovar acordo, ou quando precisar de visão consolidada do que está assinado e o que falta (MSA, DPA, NDA, SOW).
argument-hint: "<nome ou CNPJ do fornecedor/parceiro>"
---

# /verificar-fornecedor — Verificação de Fornecedor

> Consulte [CONNECTORS.md](../../CONNECTORS.md).

Consolida o status de relacionamentos contratuais com fornecedor/cliente/parceiro em todos os sistemas conectados. Identifica lacunas documentais, prazos próximos e itens de compliance.

**Vedação à alucinação.** Apenas documentos e dados **efetivamente localizados** nos sistemas conectados são reportados. Ausências são explicitadas como "não localizado". Certidões emitidas por órgãos públicos exigem consulta direta aos portais (a IA não presume validade).

## Invocação

```
/verificar-fornecedor [nome / CNPJ]
```

## Fluxo

### Fase 1 — Identificação da contraparte

Normalizar identificação:
- **Razão social** e eventuais nomes fantasia
- **CNPJ** — verificar matriz e filiais
- **Grupo econômico** — controladora, controladas, coligadas
- **Histórico de alteração societária** (cisão, incorporação, fusão, mudança de razão social)

### Fase 2 — Varredura documental

Consultar em paralelo:

- **`~~CLM`** — todos os contratos registrados (MSA, SOW, DPA, NDA, Amendments, Renovação)
- **`~~armazenamento`** — pastas do relacionamento (contratos, correspondência, dossiê)
- **`~~email`** — histórico de comunicações, notificações, tratativas
- **`~~CRM`** — oportunidades, pipeline, histórico comercial
- **`~~gestão`** — tickets abertos envolvendo a contraparte

Extrair, para cada documento localizado:
- Tipo (MSA, SOW, DPA, NDA, Aditivo)
- Data de celebração
- Vigência (início e término)
- Renovação automática
- Valores e escopo
- Responsáveis de cada lado
- Localização do original assinado

### Fase 3 — Compliance e due diligence

Verificar (ou registrar necessidade de verificar) em portais oficiais — a IA **não presume validade**, apenas sinaliza:

- **Situação cadastral** (CNPJ) — Receita Federal (ativo / suspenso / inapto / baixado)
- **Certidão Conjunta Federal (RFB/PGFN)** — obrigações tributárias federais
- **Certidão Estadual** — ICMS (quando aplicável)
- **Certidão Municipal** — ISS
- **Certidão de Regularidade FGTS (CRF)** — Caixa
- **Certidão Negativa de Débitos Trabalhistas (CNDT)** — TST
- **Certidão Negativa de Falência** — distribuidor cível
- **Cadastro de Inidôneos e Suspensos (CEIS)** — CGU
- **Cadastro Nacional de Empresas Punidas (CNEP)** — CGU (Lei 12.846/2013)
- **SICAF** — se fornece ao setor público
- **Listas restritivas internacionais** (OFAC, UN, EU) — se houver exposição internacional
- **Reputação** — consulta a veículos de imprensa, reclamações no Procon, reclamações no Reclame Aqui, processos judiciais (via ferramentas pagas de busca processual — Jusbrasil, Digesto, Serpro/Datajud — apenas se conectadas)

### Fase 4 — Análise de lacunas

Para cada contraparte ativa, verificar a presença dos documentos mínimos:

- **NDA** ou cláusula de confidencialidade no MSA — necessário desde a fase de prospecção
- **MSA** (contrato-quadro)
- **SOW/OS** para cada prestação específica
- **DPA** — obrigatório sempre que houver tratamento de dados pessoais pela contraparte (LGPD art. 39)
- **Procurações** vigentes
- **Ato constitutivo** atualizado
- **Aditivos** eventuais

### Fase 5 — Prazos e pendências

- **Vigências** a expirar nos próximos 30/60/90/180 dias
- **Renovações automáticas** (notificação prévia para não prorrogar, se for o caso)
- **Obrigações sobreviventes** (confidencialidade, LGPD, indenização) e seus termos
- **Faturamento** em aberto / inadimplência
- **SLAs** em descumprimento
- **Incidentes** de compliance registrados

## Formato de saída

```
## Verificação de Fornecedor — [razão social] (CNPJ [—])
**Data**: [—]
**Situação geral**: [Em ordem / Lacunas identificadas / Pendências críticas]

### 1. Identificação
- Razão social: [—]
- CNPJ: [—]
- Grupo econômico: [—]
- Natureza do relacionamento: [fornecedor / cliente / parceiro]
- Responsável interno: [—]

### 2. Documentos localizados
| Tipo | Data | Vigência | Valor | Localização | Responsável |
|------|------|----------|-------|-------------|-------------|
| NDA | | | | ~~armazenamento/... | — |
| MSA | | | | | |
| DPA | | | | | |
| SOW | | | | | |

### 3. Lacunas documentais
- [ ] NDA
- [ ] MSA
- [ ] DPA (há tratamento de dados pessoais?)
- [ ] Procuração vigente
- [ ] Ato constitutivo atualizado

### 4. Compliance — situação
| Item | Status | Fonte / data | Observação |
|------|--------|--------------|------------|
| CNPJ ativo | [a verificar no portal RFB] | | |
| CND Federal | | | |
| CND Estadual | | | |
| CND Municipal | | | |
| FGTS | | | |
| CNDT | | | |
| CEIS | | | |
| CNEP | | | |
| OFAC/sanções | | | |
| Falência | | | |

### 5. Prazos próximos
- [prazo] — [documento] — [data-limite] — [ação recomendada]

### 6. Obrigações sobreviventes
[Confidencialidade, LGPD, indenização, PI — termos e prazos]

### 7. Pendências / incidentes
[Inadimplência, SLAs descumpridos, incidentes de compliance]

### 8. Recomendações
- **Imediato**: [—]
- **Curto prazo (≤ 30 dias)**: [—]
- **Médio prazo**: [—]

### 9. Lacunas de informação
[Dados que não puderam ser verificados — indicar portais/sistemas a consultar manualmente]
```

## Observações

- **Validade de certidões** exige consulta direta aos portais oficiais. A IA registra a necessidade, não presume status.
- **Due diligence reforçada** para contratos com Administração Pública (Lei 14.133/2021 — art. 62 e ss.; programa de integridade obrigatório para contratos de grande vulto — art. 25, §4º).
- **LGPD** — havendo tratamento de dados pessoais pela contraparte, a ausência de DPA é **lacuna crítica** (art. 39 LGPD).
- **Sigilo** — matéria submetida a sigilo profissional; relatório para uso interno.
- **Linguagem técnica, formal, PT-BR culto.**
