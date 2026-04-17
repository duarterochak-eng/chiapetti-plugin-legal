---
name: legal-response
description: Gera respostas padronizadas a consultas jurídicas recorrentes, com verificação automática de escalonamento quando o caso não comportar resposta por template. Use para responder a requisições de titular de dados (LGPD art. 18), notificações de hold de documentos (litigation hold), consultas de fornecedores, solicitações internas de NDA, intimações, ofícios de autoridade e questionamentos padronizados de clientes.
argument-hint: "<tipo de consulta / descrição>"
---

# /responder — Resposta Templatizada

> Consulte [CONNECTORS.md](../../CONNECTORS.md).

Gera resposta padronizada a consulta jurídica recorrente, a partir de templates configurados, com verificação prévia de condições que exigiriam resposta personalizada.

**Vedação à alucinação.** O template preenche-se apenas com dados efetivamente fornecidos. Campos ausentes permanecem como **[A PREENCHER]**. Nenhuma citação de jurisprudência, doutrina ou prazo é inserida no template se não estiver prevista no modelo-base.

## Invocação

```
/responder <tipo>

Tipos suportados:
  titular-dados              # LGPD art. 18 — direitos do titular
  hold-documentos            # Preservação de documentos (litigation hold)
  nda-padrao                 # Envio de NDA-padrão da casa
  consulta-interna           # Resposta a consulta interna de unidade de negócio
  oficio-autoridade          # Resposta a ofício (Polícia, MP, Receita, ANPD, CVM)
  cancelamento-cobranca      # Resposta a reclamação de cobrança indevida (CDC)
  notificacao-extrajudicial  # Resposta a notificação extrajudicial
```

## Fluxo

### Fase 1 — Triagem para escalonamento

Antes de aplicar qualquer template, verificar se o caso **não** comporta resposta automatizada. Critérios de escalonamento (a resposta por template é **abortada**):

- **Titular de dados**: requisição envolve dados sensíveis, menor de idade, acesso a sistemas críticos, operação internacional, pedido já denegado anteriormente, ou requisição atípica (eliminação integral de dados em contexto com obrigação legal de retenção — art. 16 LGPD)
- **Hold de documentos**: mencionado processo criminal, investigação em andamento, CPI, operação da PF, Receita ou MP; envolver executivo-chave da casa/cliente; risco reputacional significativo
- **NDA**: contraparte entidade pública, estrangeira, em setor regulado com impedimentos específicos (financeiro, saúde), ou já houve recusa anterior da minuta-padrão
- **Ofício de autoridade**: ofício sem indicação clara de base legal, sem número de procedimento, fora de prazo razoável, ou com exigência desproporcional — escalar a coordenador
- **Notificação extrajudicial**: ameaça concreta de litígio, pedido de valor relevante (conforme alçada da casa), envolvendo cláusula compromissória (arbitragem — Lei 9.307/96)

Se escalonar: a IA **não emite** resposta, mas produz **ficha de escalonamento** com síntese, lacunas e recomendação.

### Fase 2 — Coleta de dados

Para o template aplicável, coletar:

- Identificação completa do destinatário (nome/razão social, CPF/CNPJ, endereço, contato)
- Número do protocolo/processo/procedimento
- Data de recebimento
- Documentos comprobatórios de identidade (LGPD)
- Prazo legal aplicável
- Base legal ou contratual da resposta
- Dados adicionais específicos do template

### Fase 3 — Preenchimento

Aplicar o template com os dados coletados. Campos faltantes permanecem como **[A PREENCHER]**.

## Templates — estrutura padrão

### Template — Titular de dados (LGPD art. 18)

```
[LOGOTIPO / TIMBRE]
[Cidade], [data]

Ao(À) Sr(a). [nome do titular]
CPF: [—]
Endereço: [—]

Ref.: Protocolo nº [—] — Requisição de Direito do Titular (LGPD art. 18, [inciso])

Prezado(a),

Em atenção à requisição protocolada em [data], exercida com fundamento no art. 18, [inciso], da Lei nº 13.709/2018 (LGPD), informamos:

[CORPO — adaptar conforme o inciso:
I — confirmação da existência de tratamento
II — acesso aos dados
III — correção de dados incompletos, inexatos ou desatualizados
IV — anonimização, bloqueio ou eliminação de dados desnecessários/excessivos/tratados em desconformidade
V — portabilidade
VI — eliminação de dados tratados com consentimento, ressalvadas as hipóteses do art. 16
VII — informação sobre compartilhamento
VIII — informação sobre a possibilidade de não fornecer consentimento e as consequências
IX — revogação do consentimento]

[LIMITAÇÕES LEGAIS APLICÁVEIS — art. 16 (retenção obrigatória) / segredo comercial e industrial / direitos de terceiros]

A resposta é emitida dentro do prazo de 15 (quinze) dias previsto no art. 19, §1º, LGPD.

Permanecemos à disposição para esclarecimentos pelo canal [—], sob responsabilidade do Encarregado pelo Tratamento de Dados Pessoais, [nome, contato].

Atenciosamente,
[Encarregado / signatário]
```

### Template — Hold de documentos (preservação de provas)

```
COMUNICADO INTERNO DE PRESERVAÇÃO DE DOCUMENTOS — [caso]

De: Departamento Jurídico
Para: [destinatários — áreas/pessoas-chave]
Data: [—]
Classificação: CONFIDENCIAL — PRIVILÉGIO PROFISSIONAL

1. Objeto
Em razão de [descrição breve — notificação extrajudicial / litígio em curso / investigação interna / procedimento administrativo], comunica-se a obrigação de preservar, sem alteração, descarte ou destruição, toda e qualquer documentação (física ou eletrônica) relacionada a [escopo].

2. Escopo da preservação
- [documentos contratuais]
- [e-mails entre X e Y no período A-B]
- [registros de sistema / logs / backups]
- [comunicações em aplicativos corporativos]
- [documentos físicos em arquivo]
- [qualquer outro material relacionado, ainda que indiretamente]

3. Duração
A obrigação vigora desde esta data e permanece até comunicação expressa em contrário pelo Departamento Jurídico.

4. Base legal/contratual
Art. 396 CPC (exibição de documento); dever processual de boa-fé (art. 5º CPC); eventual dever de guarda contratual aplicável; dever geral de colaboração com autoridades competentes.

5. Responsabilidades
Cada destinatário é responsável por: (i) aplicar o hold às suas bases; (ii) comunicar subordinados relevantes; (iii) suspender rotinas automáticas de descarte que alcancem o escopo (ex.: regras de retenção de e-mail, rotação de backups); (iv) confirmar ciência e adesão ao hold por resposta a este comunicado.

6. Canal de dúvidas
[contato]

Atenciosamente,
[signatário]
```

### Template — Ofício de autoridade

```
[TIMBRE]
[Cidade], [data]

Ilustríssimo(a) Senhor(a) [cargo / autoridade]
[órgão]
Ref.: Ofício nº [—], Procedimento [—]

Em atenção ao ofício em epígrafe, recebido em [data], vem [nome/razão social], pelo procurador signatário, apresentar o que segue:

1. [Esclarecimento / documentos anexos / solicitação de prorrogação de prazo com fundamento — se cabível]
2. Observa-se que [eventual ressalva sobre sigilo profissional — art. 7º, XIX, Lei 8.906/94; sigilo bancário — LC 105/2001; sigilo de dados — LGPD; sigilo empresarial — art. 206 Lei 9.279/96; quando aplicável]
3. Documentos anexos: [—]

Permanecemos à disposição.

Atenciosamente,
[procurador — OAB/UF]
```

### Template — Cancelamento de cobrança indevida (CDC)

```
[Cidade], [data]

Ao Sr(a). [consumidor]

Ref.: Reclamação protocolada em [data] — cobrança indevida

Em resposta à reclamação em epígrafe, reconhecida a cobrança indevida no valor de R$ [—], comunicamos:

1. O cancelamento integral do débito, com baixa nos registros internos e nos órgãos de proteção ao crédito [SPC/Serasa] se aplicável, em até [5] dias úteis.
2. A devolução do valor eventualmente pago em dobro, com correção monetária pelo INPC e juros de mora de 1% a.m., nos termos do art. 42, parágrafo único, do CDC, observada a interpretação do STJ firmada no Tema 929 (engano justificável afasta a dobra; má-fé não é exigida).
3. O envio de [carta de quitação / comprovante de exclusão] pelo canal [—] em até [—] dias.
4. Pedido formal de desculpas pelo transtorno causado.

Permanecemos à disposição pelo canal [—].

Atenciosamente,
[—]
```

### Template — Consulta interna

```
PARECER INTERNO Nº [—]

Solicitante: [área / pessoa]
Data: [—]
Assunto: [—]

1. Objeto
[Reformulação técnica da consulta]

2. Contexto fornecido
[Síntese dos fatos reportados pelo solicitante]

3. Análise
[Fundamentação com dispositivos legais efetivamente aplicáveis, com referência precisa. Sem citações inventadas.]

4. Conclusão e recomendação
[—]

5. Lacunas
[Informações que seriam necessárias para conclusão mais segura]

Atenciosamente,
[signatário]
```

## Formato de saída

Dois modos:

**(a) Resposta apta** — a IA retorna o documento preenchido, com campos não informados marcados **[A PREENCHER]**, seguido de:

```
### Dados utilizados
[—]

### Campos pendentes
[—]

### Prazo de resposta
[—]

### Recomendação de revisão humana
[sempre]
```

**(b) Escalonamento** — a IA retorna ficha de escalonamento:

```
## Escalonamento — [tipo]
**Motivo**: [critério acionado]
**Síntese**: [—]
**Documentos recebidos**: [—]
**Lacunas**: [—]
**Recomendação**: [a quem encaminhar; por que não comporta template]
```

## Observações

- **Toda resposta é minuta** — exige revisão do advogado responsável antes do envio.
- **Linguagem formal, PT-BR culto.**
- **Sigilo profissional** (art. 7º, XIX, Lei 8.906/94) preservado em todas as comunicações; marcações de confidencialidade aplicadas.
- **Prazos** computados em dias úteis ou corridos conforme a base legal aplicável (CPC — dias úteis, art. 219; LGPD — dias corridos, salvo disposição expressa).
