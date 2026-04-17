---
name: compliance-check
description: Executa verificação de compliance sobre uma ação proposta, feature de produto ou iniciativa de negócio, mapeando regulações aplicáveis, aprovações exigidas e áreas de risco no ordenamento brasileiro (LGPD, CDC, Lei Anticorrupção, regulação setorial — BACEN, CVM, ANS, ANVISA, ANATEL, CADE). Use antes do lançamento de produto, feature com dados pessoais, contratação pública, operação societária, ou iniciativa com implicações regulatórias.
argument-hint: "<descrição da ação / feature / iniciativa>"
---

# /verificar-compliance — Verificação de Compliance

> Consulte [CONNECTORS.md](../../CONNECTORS.md).

Mapeia regulações aplicáveis e exigências de compliance para ação proposta no ordenamento brasileiro. Aborda transversalmente: **LGPD** (Lei 13.709/2018), **CDC** (Lei 8.078/90), **Lei Anticorrupção** (Lei 12.846/2013 e Dec. 11.129/2022), **Lei das Estatais** (Lei 13.303/2016 quando aplicável), **Lei de Licitações** (Lei 14.133/2021), regulação setorial (BACEN, CVM, SUSEP, ANS, ANVISA, ANATEL, ANEEL, ANTT, ANAC, CADE, IBAMA, etc.), obrigações trabalhistas (CLT, NR-1, PGR, eSocial) e obrigações tributárias relevantes.

**Vedação à alucinação.** A IA cita **apenas** dispositivos de direito positivo vigente (com referência precisa) e documentos/políticas internas efetivamente localizadas. **Jamais** presume entendimento regulatório sem fonte — se o caso exigir consulta formal, recomenda consulta dedicada à autoridade ou parecer de especialista.

## Invocação

```
/verificar-compliance [descrição da ação]
```

## Fluxo

### Fase 1 — Escopo

Capturar, via `~~email`, `~~armazenamento`, `~~chat` ou resposta do usuário:

- **Natureza** da ação (lançamento de feature, contratação, parceria, operação societária, campanha publicitária, expansão geográfica)
- **Setor** envolvido
- **Dados pessoais** tratados (categorias, titulares, finalidade)
- **Público-alvo** (consumidor, B2B, criança/adolescente, idoso, pessoa em situação de vulnerabilidade)
- **Geografia** (UFs envolvidas, transferência internacional de dados)
- **Parceiros/fornecedores**
- **Cronograma**

### Fase 2 — Mapeamento regulatório

#### LGPD (sempre verificar)
- **Hipótese legal** (art. 7º e art. 11 — dado sensível) — consentimento, execução de contrato, cumprimento de obrigação legal, interesse legítimo, proteção da vida, tutela da saúde, execução de políticas públicas, estudo por órgão de pesquisa, exercício regular de direitos, proteção ao crédito
- **Princípios** (art. 6º — finalidade, adequação, necessidade, livre acesso, qualidade, transparência, segurança, prevenção, não discriminação, responsabilização)
- **Direitos do titular** (art. 18)
- **Tratamento de dados sensíveis** (art. 11) — biométrico, saúde, genético, racial/étnico, religioso, filiação sindical, filosófico, orientação sexual, vida sexual
- **Crianças e adolescentes** (art. 14)
- **Transferência internacional** (arts. 33-36) — decisão de adequação da ANPD, cláusulas-padrão, normas corporativas globais, cooperação internacional, proteção da vida, consentimento específico
- **Operador / compartilhamento** — DPA (Contrato de Tratamento de Dados) firmado; subcontratação com anuência
- **Encarregado (DPO)** designado — art. 41
- **Relatório de Impacto à Proteção de Dados (RIPD)** quando exigível — art. 38
- **Plano de resposta a incidentes** (Res. ANPD 15/2024)

#### CDC (sempre verificar se houver relação de consumo)
- **Direito à informação** (art. 6º, III) — clareza, precisão
- **Publicidade** (arts. 36-38) — princípio da identificação, vedação à publicidade enganosa/abusiva
- **Cláusulas abusivas** (art. 51) — foro de eleição desfavorável, limitação indenizatória em consumo, inversão do ônus, renúncia a direito
- **Direito de arrependimento** (art. 49) — 7 dias para compras fora do estabelecimento
- **SAC** (Dec. 11.034/2022)
- **Atendimento a grupos vulneráveis** (idoso, criança, PcD — Lei 10.741/2003 (Estatuto do Idoso); Lei 13.146/2015 (LBI))

#### Lei Anticorrupção (sempre verificar em transações com agente público ou parceiro exposto)
- **Responsabilização objetiva** (art. 2º) — responsabilidade civil e administrativa
- **Atos lesivos** (art. 5º)
- **Programa de integridade** (Dec. 11.129/2022 — elementos: alta direção, código de conduta, treinamento, canal de denúncias, controles internos, due diligence de terceiros, gestão de riscos, investigação, apuração e sanções)
- **Acordo de leniência** (arts. 16-17)
- **Due diligence de terceiros** — especialmente em setores regulados, licitações e exportação

#### Licitações (Lei 14.133/2021, se contratação com Administração Pública)
- Modalidades, regime de contratação, habilitação (arts. 62-70), exigências documentais, programa de integridade obrigatório para contratos de grande vulto (art. 25, §4º)

#### Regulação setorial (verificar conforme setor)
- **Financeiro** — BACEN (Res. CMN/BCB, circulares BACEN), CVM (instruções e resoluções, Res. CVM 80 — prestadores de serviço, Res. CVM 44 — fato relevante), SUSEP
- **Saúde suplementar** — ANS (RN 465/2021 rol, RN 259/2011 prazos, LGPD saúde)
- **Telecom** — ANATEL
- **Energia** — ANEEL
- **Saúde / alimentos / cosméticos** — ANVISA
- **Transporte** — ANTT, ANAC
- **Defesa da concorrência** — CADE (Lei 12.529/2011, controle de estruturas — Res. CADE 33, controle de condutas, guia de compliance)
- **Meio ambiente** — IBAMA, órgãos estaduais (licenciamento, Lei 6.938/81)

#### Trabalhista
- **CLT** — contratação, jornada (arts. 58-75), férias (arts. 129-153), rescisão (arts. 477-486), terceirização (Lei 13.429/2017)
- **NR-1** (PGR), **NR-5** (CIPA), demais NRs conforme o setor
- **eSocial** — obrigações acessórias

### Fase 3 — Risco e recomendações

Classificação de risco inicial (provável/possível/remoto em linha com CPC 25 — Provisões, Passivos e Ativos Contingentes) e encaminhamento:

- **Aprovações internas** necessárias (jurídico, DPO, compliance, alta direção)
- **Aprovações/notificações externas** necessárias (ANPD — comunicação de incidente, CADE — ato de concentração, CVM — fato relevante, ANS — credenciamento, órgãos ambientais — licenciamento)
- **Documentos** a elaborar (RIPD, DPA, contratos, códigos, políticas, treinamentos)

## Formato de saída

```
## Verificação de Compliance — [ação]

### 1. Escopo
- **Ação**: [—]
- **Setor**: [—]
- **Público**: [—]
- **Dados pessoais tratados**: [sim/não; categorias]
- **Transferência internacional**: [sim/não]
- **Cronograma**: [—]

### 2. Mapeamento regulatório
#### LGPD
[Base legal indicada, obrigações, RIPD exigível?]

#### CDC (se aplicável)
[—]

#### Lei Anticorrupção
[—]

#### Regulação setorial
[—]

#### Trabalhista / tributário / ambiental (se aplicável)
[—]

### 3. Riscos identificados
| Risco | Severidade | Probabilidade | Mitigação |
|-------|-----------|---------------|-----------|

### 4. Aprovações internas exigidas
[—]

### 5. Aprovações/notificações externas
[—]

### 6. Documentos a elaborar
[RIPD, DPA, contratos, políticas, treinamento, código de conduta]

### 7. Cronograma de compliance
[—]

### 8. Lacunas e recomendações de pesquisa dedicada
[Pontos que exigem consulta formal à autoridade ou parecer de especialista]
```

## Observações

- **Linguagem técnica, formal, PT-BR culto.**
- **Jamais inventar** interpretação da autoridade (ANPD, CVM, CADE). Quando a questão for cinzenta, recomendar consulta formal.
- **Sigilo.** Documentos e dados analisados devem ser tratados como matéria submetida a sigilo profissional.
- Acionar `/avaliar-risco` para aprofundamento de risco específico.
