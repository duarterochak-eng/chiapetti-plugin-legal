---
name: signature-request
description: Prepara e roteia documento para assinatura eletrônica — checklist pré-assinatura, configuração de ordem de assinatura, envio para execução. Alinhado à MP 2.200-2/2001 (ICP-Brasil) e à Lei 14.063/2020 (assinaturas simples, avançada e qualificada). Suporta plataformas do mercado brasileiro (Clicksign, D4Sign, ZapSign) e internacional (DocuSign, Adobe Sign). Use quando contrato finalizado estiver pronto para assinar, ao verificar entidades, anexos e blocos de assinatura antes do envio, ou ao configurar envelope com signatários sequenciais ou paralelos.
argument-hint: "<documento / contrato finalizado>"
---

# /solicitar-assinatura — Solicitação de Assinatura Eletrônica

> Consulte [CONNECTORS.md](../../CONNECTORS.md).

Roteia documentos para assinatura eletrônica seguindo os requisitos legais brasileiros de validade.

**Vedação à alucinação.** Nenhum signatário, representante, procuração ou dado é presumido — tudo é confirmado com o solicitante antes do envio. Lacunas explicitadas.

## Arcabouço legal

- **MP 2.200-2/2001** — Infraestrutura de Chaves Públicas Brasileira (ICP-Brasil); presunção de autoria e integridade do documento assinado com certificado ICP-Brasil (art. 10, §1º). Uso de outras formas de comprovação de autoria também admitido desde que aceito pelas partes (art. 10, §2º).
- **Lei 14.063/2020** — três tipos de assinatura eletrônica:
  - **Simples**: permite identificar o signatário e anexar/associar dados a outros dados em formato eletrônico do signatário
  - **Avançada**: utiliza certificados não emitidos pela ICP-Brasil, vinculada ao signatário de modo unívoco, permitindo detecção de alterações
  - **Qualificada**: utiliza certificado ICP-Brasil — presunção legal de autoria e integridade
- **CPC**, arts. 205, §1º; 411; 439 e 440 — documento eletrônico; Resolução CNJ 345/2020 (Juízo 100% Digital) e 385/2021
- **CC**, art. 221 — instrumento particular eficaz quando reproduzido em meio mecânico/eletrônico

Em contratos com Administração Pública, atentar a Lei 14.063/2020 quanto a exigência de assinatura avançada ou qualificada, conforme o tipo de ato.

## Invocação

```
/solicitar-assinatura [documento]
```

## Fluxo

### Fase 1 — Checklist pré-assinatura

Verificar:

1. **Versão final** do documento — não há "última versão" pendente; arquivo bate com a última minuta aprovada
2. **Razão social e CNPJ/CPF** de cada parte conferem com: (i) contrato social / estatuto social atualizado; (ii) procuração vigente; (iii) cartão CNPJ atualizado; (iv) RG/CPF dos representantes
3. **Poderes de representação** — representantes indicados possuem poderes suficientes conforme o ato constitutivo atualizado e eventuais procurações; verificar limites (alçada)
4. **Anexos** — todos os anexos citados no corpo estão presentes (SLA, anexo técnico, DPA, planilha de preços, políticas)
5. **Valor e vigência** — campos preenchidos
6. **Data da celebração** — em branco (deixar a plataforma preencher) ou conforme negociado
7. **Local** — preenchido
8. **Blocos de assinatura** — um por signatário, com nome, CPF, cargo, e-mail
9. **Testemunhas** — se o contrato for executar em sede judicial como título executivo extrajudicial (art. 784, III CPC), são exigidas 2 testemunhas
10. **Paginação e rubricas** — verificar se a plataforma aplicará hash a cada página e selo digital agregado ao final
11. **Declaração LGPD** — informar aos signatários o tratamento de seus dados (nome, CPF, e-mail, geolocalização, IP) e a base legal (art. 7º, V — execução de contrato)
12. **Identificação do tipo de assinatura** exigido (simples / avançada / qualificada — conforme a matéria e a contraparte)

### Fase 2 — Escolha de plataforma

- **ICP-Brasil** (presunção legal plena) — certificado A3 (token/smartcard) ou A1 (arquivo)
- **Clicksign / D4Sign / ZapSign** — plataformas brasileiras com múltiplos métodos (e-mail + PIN, WhatsApp, selfie + documento, ICP-Brasil integrada); armazenamento em nuvem nacional; conformidade com LGPD
- **DocuSign / Adobe Sign** — plataformas internacionais; atenção à transferência internacional de dados (arts. 33-36 LGPD)

### Fase 3 — Configuração do envelope

- **Ordem** — paralela (todos ao mesmo tempo) ou sequencial (A → B → C); se houver aprovação interna prévia (alçada), aprovador assina antes
- **Prazo** para assinatura (prazo razoável; vencido, o envelope expira e deve ser reenviado)
- **Lembretes automáticos**
- **Observadores** (CC — recebem o documento assinado)
- **Autenticação adicional** quando cabível (SMS, selfie, documento)
- **Arquivamento** — pasta em `~~armazenamento`; registro em `~~CLM`; entrada em `~~gestão`

### Fase 4 — Envio e acompanhamento

A IA prepara o envelope (via `~~assinatura`) e acompanha até a execução integral. Após assinado:

- Baixar documento final e relatório de assinatura
- Registrar em `~~CLM` com metadados (partes, valor, vigência, objeto, responsável)
- Comunicar às partes o documento executado
- Se for título executivo extrajudicial, armazenar em pasta específica para execução

## Formato de saída

```
## Solicitação de Assinatura — [contrato]
**Partes**: [—]
**Tipo de assinatura**: [simples / avançada / qualificada ICP-Brasil]
**Plataforma**: [—]
**Data**: [—]

### 1. Checklist pré-assinatura
| Item | Status | Observação |

### 2. Signatários
| Nome | CPF | Cargo | E-mail | Ordem | Poderes (fonte) |

### 3. Anexos incluídos
[—]

### 4. Configuração do envelope
- Ordem: [—]
- Prazo: [—]
- Lembretes: [—]
- Autenticação adicional: [—]

### 5. Destino pós-assinatura
- CLM: [—]
- Armazenamento: [—]
- Gestão: [—]

### 6. Pendências
[—]

### 7. Lacunas
[—]
```

## Observações

- **Revisão humana obrigatória** antes do envio.
- **Procurações** devem ser anexadas ao envelope quando o signatário atuar por procuração (registrar o ato que dá origem aos poderes — Ata, Contrato Social, Procuração com prazo vigente).
- **Títulos executivos extrajudiciais** (art. 784 CPC) — atentar aos requisitos específicos (ex.: duas testemunhas assinadas para o inciso III).
- **Sigilo e LGPD** — dados pessoais coletados pela plataforma de assinatura são tratados sob base de execução de contrato (art. 7º, V LGPD); incluir comunicação no envelope.
- **Linguagem técnica, formal, PT-BR culto.**
