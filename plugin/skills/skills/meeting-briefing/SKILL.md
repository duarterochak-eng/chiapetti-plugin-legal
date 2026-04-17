---
name: meeting-briefing
description: Prepara briefings estruturados para reuniões com relevância jurídica e acompanha itens de ação resultantes. Use para preparar audiências (AIJ, conciliação, instrução), reuniões de negociação contratual, assembleias de sócios/acionistas (AGO, AGE), reuniões com autoridades (ANPD, CVM, BACEN, MP), reuniões de comitê de crise ou qualquer encontro em que contexto jurídico, pesquisa prévia e rastreamento de ações sejam necessários.
argument-hint: "<reunião / audiência / assembleia>"
---

# /reuniao-briefing — Briefing de Reunião

> Consulte [CONNECTORS.md](../../CONNECTORS.md).

Prepara briefings estruturados para reuniões com relevância jurídica e acompanha itens de ação.

**Vedação à alucinação.** Fatos, valores, partes, cláusulas e prazos constam **apenas** se documentalmente localizados. Inferências rotuladas. Lacunas reportadas. Sem citações inventadas.

## Invocação

```
/reuniao-briefing <tipo> [identificador]

Tipos:
  audiencia               # AIJ, conciliação, instrução, sustentação oral
  negociacao-contratual   # Contrato em negociação
  assembleia              # AGO, AGE, comitê, conselho
  autoridade              # Reunião/oitiva com ANPD, CVM, BACEN, MP, RFB, Polícia
  comite-crise            # Comitê de crise (incidente, investigação)
  interna                 # Reunião interna com área cliente
```

## Fluxo

### Fase 1 — Coleta de contexto

Varrer `~~agenda`, `~~email`, `~~armazenamento`, `~~CLM`, `~~gestão`, `~~chat` para consolidar:

- **Participantes** (quem, papel, histórico de interação)
- **Pauta** (se fornecida, ou inferida do thread)
- **Documentos** relacionados (contratos, minutas, pareceres, intimações, atas anteriores)
- **Histórico do caso/relacionamento**
- **Pendências** (prazos, ações, compromissos abertos)
- **Posições internas** (playbook, alçada, limites)

### Fase 2 — Tipo-específico

#### audiencia
- **Processo** (nº CNJ, partes, valor, rito)
- **Fase atual**
- **Natureza da audiência** (AIJ, conciliação, instrução, una, sustentação oral)
- **Testemunhas arroladas** (rol em fls., qualificação, tópicos)
- **Pontos controvertidos** (saneador, art. 357 CPC)
- **Estratégia de inquirição** — linhas de perguntas a testemunhas próprias e à parte adversa; pontos a atacar na prova oral
- **Documentos a juntar / apresentar em mesa**
- **Prazo para alegações finais** (art. 364 CPC — 15 dias após encerrada a instrução, em memoriais, se complexa a causa)
- **Preposto / procuração** — verificar poderes (art. 105 CPC; mandato ad judicia et extra)

#### negociacao-contratual
- **Status da minuta** (versão, autor da última redação)
- **Cláusulas já acordadas**
- **Cláusulas em aberto** (com posições já manifestadas por cada lado)
- **Alçada de concessão interna**
- **Playbook aplicável** (responsabilidade, indenização, LGPD — DPA, foro, lei aplicável, rescisão)
- **Escalonamento** — quando cada cláusula requer aprovação superior

#### assembleia
- **Convocação** (art. 124 Lei 6.404/76 para S.A.; art. 1.152 CC para ltda.; prazos: 30 dias para 1ª convocação de AGO — art. 124 §1º, I; 8 dias para 2ª — II)
- **Pauta** — ordem do dia
- **Quórum de instalação e deliberação** (art. 125 LSA; art. 1.072 CC)
- **Voto por procuração** (art. 126 LSA; Res. CVM 81/2022 — assembleia digital e participação remota para cias abertas)
- **Documentos** — proposta da administração, relatório anual, demonstrações financeiras, parecer do conselho fiscal
- **Pontos controvertidos** — conflito de interesses (art. 115 LSA), bloqueio de voto
- **Minuta de ata**

#### autoridade
- **Órgão e autoridade** (ANPD, CVM, BACEN, CADE, MP, RFB, Polícia, outros)
- **Base legal** da convocação/oitiva (ofício, TCAC, acordo, colaboração, compromisso, termo de ajustamento)
- **Direito ao silêncio / não autoincriminação** (CF art. 5º, LXIII; em casos criminais/administrativos)
- **Sigilo profissional** (art. 7º, XIX, Lei 8.906/94)
- **Documentos a apresentar / não apresentar** (prerrogativa de análise prévia)
- **Estratégia** — acordo de leniência (Lei 12.846/2013), TCAC (Res. CVM 45), compromisso de cessação CADE, termo de ajustamento de conduta

#### comite-crise
- **Natureza do incidente** (dados pessoais, fraude, desvio, vazamento, ataque cibernético, acidente, litígio crítico)
- **Cronologia reconstituída**
- **Obrigações de comunicação** em aberto (ANPD/titulares LGPD art. 48; Res. ANPD 2/2022 e 15/2024; comunicação à autoridade conforme setor; fato relevante CVM)
- **Hold de documentos** ativo? (se não, acionar `/responder hold-documentos`)
- **Pessoas envolvidas** e representação
- **Externos contratados** (forense, auditoria, PR, jurídico externo)

#### interna
- **Solicitante** e unidade de negócio
- **Consulta** (reformulação técnica)
- **Histórico** — já houve parecer sobre a matéria
- **Urgência**

### Fase 3 — Produção do briefing

## Formato de saída

```
## Briefing de Reunião — [tipo] — [identificador]
**Data/hora**: [—]
**Local / modalidade**: [presencial / videoconferência / plataforma]
**Duração prevista**: [—]
**Participantes**:
| Nome | Papel | Observações |

### 1. Objeto da reunião
[—]

### 2. Pauta
[—]

### 3. Contexto consolidado
[Síntese factual densa com referência a documentos-fonte]

### 4. Documentos-chave (anexos / links)
[Caminhos em ~~armazenamento; peças em ~~tribunal; minutas em ~~CLM]

### 5. Posição interna / estratégia
[Conforme tipo — pontos a defender, ceder, explorar; alçada]

### 6. Riscos e pontos sensíveis
[Itens que exigem cuidado — sigilo, conflito, alçada, prazos]

### 7. Perguntas / tópicos a abordar
[Lista enxuta]

### 8. Material de apoio
[Playbook, modelos de peça, pareceres anteriores]

### 9. Pós-reunião — itens a cumprir
[—]

### 10. Lacunas identificadas
[—]
```

## Acompanhamento pós-reunião

A partir de ata, resumo ou anotações fornecidas, a IA consolida:

- **Itens de ação** — responsável, prazo, status
- **Decisões** tomadas
- **Pendências** remanescentes
- **Próxima reunião** — pauta preliminar
- **Atualização do caso** — registrar em `~~gestão`

## Observações

- **Sigilo profissional** preservado. Em reuniões com autoridade, atentar para prerrogativas do art. 7º Lei 8.906/94 (inviolabilidade do escritório, sigilo da comunicação cliente-advogado — art. 7º, §6º).
- **Linguagem técnica, formal, PT-BR culto.**
- **Jamais inventar** citações, precedentes, posições de autoridade ou teor de documentos não localizados.
