# Guia de Uso — Plugin Jurídico (legal-br)

Este guia explica, em linguagem direta, o que cada comando (skill) do plugin faz, quando usar e como usar. Para cada comando você encontra: **o que é**, **quando acionar**, **como funciona (protocolo)** e **um exemplo prático**.

> **Observação geral.** O plugin é ferramenta de apoio. Ele organiza informação, padroniza respostas e acelera análises — mas toda produção é uma minuta que precisa ser revisada pelo advogado responsável antes de sair para o cliente, contraparte, juízo ou autoridade. O plugin nunca inventa jurisprudência, doutrina ou fatos: se a informação não está nos autos ou em fonte conectada, ele avisa "não localizado".

---

## 1. `/analise-processo-pequeno` — Análise de processo pequeno (até ~100 páginas)

**O que é.** Faz a leitura integral de uma peça isolada ou de um processo pequeno (JEC, ação inicial, petição avulsa) e devolve uma síntese estruturada com teses das partes, fatos, provas, decisões, pontos críticos e recomendações.

**Quando acionar.**
- Recebeu uma petição inicial, contestação, sentença ou laudo e precisa de uma leitura técnica organizada.
- Processo em Juizado Especial Cível com autos enxutos.
- Análise pontual de uma peça específica dentro de um processo maior.

**Protocolo.**
1. Você envia o arquivo (PDF, texto, número CNJ se houver integração com tribunal).
2. O plugin pergunta o objetivo (vou recorrer? preciso elaborar contestação? é parecer de viabilidade?).
3. Faz leitura integral, identifica teses, fatos provados e controvertidos, matriz probatória e eventuais preliminares.
4. Devolve um relatório estruturado em seções: identificação, síntese factual, teses de cada parte, decisões, análise técnica, inconsistências, prazos, recomendação e eventual minuta preliminar.

**Exemplo prático.** "Cheguei com uma sentença de 60 páginas em ação de cobrança. Rodei `/analise-processo-pequeno` com a sentença e o contrato anexo. Em minutos tinha a síntese dos fundamentos do juiz, os pontos vulneráveis para recurso (prescrição não analisada, perícia desconsiderada sem motivação suficiente) e um esqueleto de razões de apelação para eu revisar."

---

## 2. `/analise-processo-medio` — Análise de processo médio (~100 a 1000 páginas)

**O que é.** Para processos em rito ordinário com volume intermediário. Em vez de ler tudo de uma vez e perder profundidade, o plugin monta um índice dos autos, lê em camadas (peças centrais, provas, depois movimentações acessórias) e produz análise completa.

**Quando acionar.**
- Processo cível, trabalhista, tributário ou administrativo em fase de instrução ou recursal com várias peças, laudos e decisões.
- Você precisa preparar apelação, memoriais, sustentação oral ou parecer técnico.

**Protocolo.**
1. Envia os autos e informa o objetivo (peça a elaborar, prazo, foco).
2. O plugin pergunta se há áreas prioritárias (mérito × processual, prescrição, perícia específica).
3. Constrói um índice cronológico de todas as peças (data, autor, natureza, folhas).
4. Lê em três camadas: (a) peças centrais — inicial, contestação, saneador, sentença, recursos; (b) provas determinantes — laudos, depoimentos, documentos-chave; (c) movimentações acessórias para controle de cronologia e prazos.
5. Devolve análise técnica completa com matriz probatória, decisões analisadas, riscos, recomendação estratégica e, se pedido, minuta preliminar.

**Exemplo prático.** "Assumi um processo trabalhista com 400 páginas, quatro volumes, depois que o colega saiu do escritório. Rodei `/analise-processo-medio` pedindo foco em horas extras e nulidades do saneador. Recebi o índice dos autos, quem já foi ouvido, o que o perito concluiu, pontos que o juiz fixou como controvertidos e os pontos frágeis da defesa da empresa. Usei como base para preparar a sustentação oral."

---

## 3. `/analise-processo-extenso` — Análise de processo extenso (1000+ páginas)

**O que é.** Para autos muito volumosos — recuperações judiciais, ações coletivas, processos tributários com milhares de páginas, arbitragens complexas, M&A contencioso. Usa estratégia de fragmentação hierárquica para não perder nada e manter cada afirmação rastreável à folha de origem.

**Quando acionar.**
- Qualquer processo acima de 1000 páginas.
- Processos com múltiplos apensos, cadernos e anexos.
- Recuperações judiciais (Lei 11.101/2005), ACP, ações coletivas.

**Protocolo.**
1. Briefing inicial: objetivo, prazo, foco temático, apensos, histórico interno.
2. Inventário: lista todos os arquivos, páginas e estrutura dos autos.
3. Divide o material em blocos lógicos (peças inaugurais, instrução, perícias, audiências, decisões, recursos, incidentes, apensos).
4. Faz duas passadas: uma extraindo as informações brutas de cada unidade; outra consolidando em resumos por camada (unidade → sub-bloco → bloco → visão integral).
5. Analisa por eixos: factual, jurídico, processual, probatório, recursal, temporal.
6. Fecha com recomendação estratégica, riscos, minuta preliminar (se pedida) e lista de lacunas.

**Exemplo prático.** "Recebemos um processo de recuperação judicial com 3200 páginas, três cadernos de habilitação de crédito e dois apensos de impugnação. Rodei `/analise-processo-extenso` pedindo foco nas impugnações apresentadas pelo nosso cliente. Em etapas, o plugin entregou o índice-mestre, as sínteses por bloco, a matriz de teses, identificou decisões pendentes de recurso e apontou que faltavam nos autos três anexos citados em uma das impugnações — lacuna que precisava ser sanada antes da assembleia de credores."

---

## 4. `/brief` — Briefing jurídico

**O que é.** Três modos de briefing: **diário** (panorama da manhã), **temático** (pesquisa interna sobre um assunto) e **incidente** (situação em desenvolvimento que pede contexto rápido).

**Quando acionar.**
- Início do dia, para ver o que precisa de atenção antes das reuniões.
- Quando o cliente liga com uma dúvida nova e você quer saber se o escritório já tratou do tema.
- Quando surge uma crise (vazamento de dados, oficial de justiça na porta, reclamação pública).

**Protocolo (diário).** Varre e-mail, agenda, contratos e sistemas conectados. Devolve: prazos processuais da semana, audiências do dia, publicações recentes, contratos com vencimento próximo, alertas regulatórios e consultas internas pendentes.

**Protocolo (temático).** Busca em pastas, e-mails, contratos e sistema de gestão para localizar pareceres anteriores, minutas, precedentes internos, e-mails relevantes. Não inventa jurisprudência externa — se precisar, recomenda pesquisa dedicada.

**Protocolo (incidente).** Reconstrói cronologia, identifica documentos envolvidos, pessoas, obrigações imediatas de comunicação (ANPD, CVM, BACEN conforme o caso) e próximos passos.

**Exemplos práticos.**
- Diário: "7h da manhã, rodei `/brief diario`. Descobri que tinha audiência às 14h que não estava no meu calendário pessoal (estava só no do advogado júnior) e um contrato vencendo sexta que eu tinha esquecido."
- Temático: "Cliente perguntou sobre possibilidade de usar arbitragem em contrato com estatal. Rodei `/brief tema arbitragem com estatal`. Achou dois pareceres internos de 2023 e uma minuta que já tínhamos usado."
- Incidente: "Cliente ligou às 22h dizendo que sofreu invasão no sistema e dados de clientes vazaram. Rodei `/brief incidente vazamento de dados — cliente X`. Em cinco minutos tinha a cronologia, a lista de obrigações LGPD (comunicação à ANPD, aos titulares) e os próximos passos prioritários."

---

## 5. `/verificar-compliance` — Verificação de compliance

**O que é.** Mapeia tudo o que a legislação brasileira exige antes de uma ação nova (lançamento de produto, feature, contratação, parceria, operação societária). Cobre LGPD, CDC, Lei Anticorrupção, Lei das Estatais, Licitações, regulação setorial (BACEN, CVM, ANS, ANVISA, ANATEL, CADE, etc.) e obrigações trabalhistas e tributárias.

**Quando acionar.**
- Antes de colocar uma feature nova no ar, especialmente se envolve dados pessoais.
- Antes de lançar campanha publicitária.
- Antes de assinar contrato com fornecedor exposto a risco reputacional ou em setor regulado.
- Antes de uma operação societária (compra, venda, fusão).

**Protocolo.**
1. Descreve a ação, o setor, o público-alvo, os dados pessoais envolvidos e a geografia.
2. O plugin passa um pente fino em cada arcabouço aplicável: LGPD (base legal, princípios, direitos do titular, transferência internacional, incidentes), CDC (direito à informação, publicidade, cláusulas abusivas, atendimento), Anticorrupção (responsabilização objetiva, programa de integridade, due diligence), setorial (conforme o caso).
3. Classifica o risco e indica aprovações internas necessárias, comunicações externas (ANPD, CVM, CADE) e documentos a elaborar (RIPD, DPA, políticas).

**Exemplo prático.** "Nosso cliente fintech quer lançar um produto novo que analisa histórico de crédito do usuário via open finance. Rodei `/verificar-compliance open finance análise crédito B2C`. O plugin listou obrigações LGPD (base legal, RIPD obrigatório, comunicação de incidente), BACEN (Resolução sobre open finance), CDC (informação clara sobre uso dos dados) e a necessidade de DPA com a instituição que fornece os dados. Virou checklist para a área de produto."

---

## 6. `/responder` — Resposta templatizada

**O que é.** Gera respostas padronizadas para consultas jurídicas que se repetem: titular de dados LGPD, hold de documentos, envio de NDA-padrão, ofício de autoridade, reclamação de cobrança indevida, consulta interna, notificação extrajudicial. Antes de aplicar o template, verifica se o caso é simples o bastante para resposta automática ou se precisa de escalonamento.

**Quando acionar.**
- Requisição de titular de dados (LGPD art. 18) chegou no canal do DPO.
- Área de negócio precisa de uma NDA-padrão do escritório para mandar a um prospect.
- Ofício de autoridade (PF, MP, Receita, ANPD) chegou e precisa de primeira resposta padrão.
- Cliente reclamou de cobrança indevida e você quer responder no prazo com a estrutura correta.

**Protocolo.**
1. Você indica o tipo de resposta (titular-dados, hold-documentos, nda-padrao, oficio-autoridade, cancelamento-cobranca, consulta-interna, notificacao-extrajudicial).
2. O plugin verifica se o caso comporta template ou se deve ser escalado (envolve dados sensíveis, menor de idade, processo criminal, contraparte estrangeira, pedido atípico).
3. Coleta os dados mínimos (destinatário, número do protocolo, prazo, base legal).
4. Entrega a minuta com campos marcados `[A PREENCHER]` onde faltam dados.

**Exemplo prático.** "Titular requereu exclusão completa dos dados pessoais (art. 18, VI, LGPD). Rodei `/responder titular-dados`. O plugin confirmou que cabia template (não envolvia dado sensível nem criança), coletou os dados do titular e do protocolo, e devolveu uma minuta de resposta dentro do prazo de 15 dias do art. 19 da LGPD, com a ressalva sobre os dados de retenção obrigatória do art. 16. Fiz ajustes pontuais e enviei."

---

## 7. `/avaliar-risco` — Avaliação de risco jurídico

**O que é.** Classifica o risco de um contrato, litígio ou contingência segundo uma matriz de **severidade × probabilidade**, alinhada ao CPC 25 (provável / possível / remoto) para fins contábeis. Sugere mitigação, responsável e provisão, quando cabível.

**Quando acionar.**
- Avaliação de exposição em contrato que está para ser fechado.
- Classificação de contingências para reporte contábil trimestral.
- Decisão de negócio com implicações regulatórias.
- Triagem inicial antes de escalar para sócio ou parecer externo.

**Protocolo.**
1. Você descreve o caso: partes, valor, documentos, estágio, histórico.
2. O plugin avalia duas dimensões:
   - **Severidade**: impacto financeiro, criminal, regulatório, reputacional, operacional (baixo / médio / alto / crítico).
   - **Probabilidade**: muito baixa → muito alta, com base nos fatos e em eventual jurisprudência efetivamente localizada (nada é inventado).
3. Cruza na matriz e entrega a classificação (B/M/A/C), a fundamentação, a sugestão de provisão contábil (CPC 25) e se cabe reporte regulatório (fato relevante CVM, comunicação LGPD à ANPD, CADE, ANS).

**Exemplo prático.** "Recebi ação trabalhista nova, pedido de R$ 1,2 milhão, cliente industrial. Rodei `/avaliar-risco`. O plugin cruzou os fatos (jornada admitida em contestação, testemunhas já arroladas, função de confiança discutível), pediu documentos que eu ainda não tinha (cartões de ponto, recibos de horas extras) e classificou como risco médio com probabilidade média — possível (CPC 25). Sugeriu provisão equivalente a 40% do pedido pendente do resultado da prova oral."

---

## 8. `/reuniao-briefing` — Briefing de reunião

**O que é.** Prepara briefing estruturado para qualquer reunião com relevância jurídica — audiência, negociação contratual, assembleia, oitiva com autoridade, comitê de crise, reunião interna — e depois acompanha os itens de ação que ficaram.

**Quando acionar.**
- Antes de uma audiência: quer o histórico do processo, pontos controvertidos, testemunhas e estratégia.
- Antes de negociar um contrato: status da minuta, cláusulas acordadas, alçada.
- Antes de AGO/AGE: convocação, pauta, quórum, conflito de interesses.
- Antes de oitiva em autoridade: base da convocação, direito ao silêncio, documentos a apresentar.

**Protocolo.**
1. Você indica o tipo de reunião e o identificador (processo, contrato, empresa, autoridade).
2. O plugin puxa contexto de agenda, e-mail, pasta do caso, CLM e sistema de gestão.
3. Entrega briefing com: objeto, pauta, participantes, contexto consolidado, documentos-chave, estratégia, pontos sensíveis, perguntas a abordar, material de apoio e próximos passos.
4. Depois da reunião, a partir da ata ou das suas anotações, consolida itens de ação com responsável e prazo.

**Exemplo prático.** "Tinha AIJ às 9h no dia seguinte, processo com 300 páginas que eu não tinha tempo de reler. Rodei `/reuniao-briefing audiencia` com o número do processo. De manhã, tinha o saneador, os pontos controvertidos, o rol de testemunhas, sugestões de linhas de inquirição para cada uma e os documentos mais importantes juntados no mês anterior. Fui para audiência preparado em uma hora."

---

## 9. `/revisar-contrato` — Revisão contratual

**O que é.** Revisa um contrato cláusula a cláusula contra o playbook do escritório (posições-padrão). Aponta desvios, gera red-lines (sugestões de redação) e organiza as prioridades de negociação.

**Quando acionar.**
- Recebeu minuta de fornecedor ou cliente.
- Precisa preparar estratégia de negociação com o que é inegociável, o que pode ceder e o que é aceitável.
- Quer conferência sistemática antes de assinar.

**Protocolo.**
1. Identifica a natureza do contrato (prestação de serviços, M&A, consumo, administrativo, etc.) e o regime jurídico aplicável.
2. Passa pelo check-list estrutural do Código Civil (capacidade, objeto lícito, forma) e legislação especial conforme o caso (CDC, Lei 14.133/2021, Lei das S.A.).
3. Analisa cláusula a cláusula: objeto, preço, prazo, rescisão, limitação de responsabilidade, indenização, confidencialidade, LGPD/DPA, propriedade intelectual, anticorrupção, cessão, foro e lei.
4. Gera quadro-resumo com desvio × posição playbook × sugestão × prioridade, red-lines e nota de negociação.

**Exemplo prático.** "Fornecedor mandou o próprio MSA, 40 páginas, responsabilidade ilimitada do nosso cliente, foro em São Paulo (cliente está em Curitiba), sem DPA. Rodei `/revisar-contrato`. Em 20 minutos tinha o quadro com 14 desvios do playbook, prioridades classificadas (crítico: limitação de responsabilidade e DPA; alto: foro; médio: prazo de rescisão), red-lines prontas para track changes e argumentos de negociação para cada um. Mandei para revisão do sócio."

---

## 10. `/solicitar-assinatura` — Solicitação de assinatura eletrônica

**O que é.** Prepara o documento para assinatura eletrônica, confere tudo antes de enviar (razão social, CNPJ, poderes, anexos) e configura o envelope na plataforma escolhida (Clicksign, D4Sign, ZapSign, DocuSign, ICP-Brasil). Alinhado à MP 2.200-2/2001 e à Lei 14.063/2020 (assinatura simples, avançada e qualificada).

**Quando acionar.**
- Contrato finalizado, pronto para assinar.
- Conferência pré-envio para não mandar envelope com erro.
- Quando há múltiplos signatários e a ordem importa.

**Protocolo.**
1. Confere: versão final confere com a última aprovada, razão social e CNPJ batem com contrato social atualizado, representantes têm poderes, todos os anexos estão juntos, valor e vigência preenchidos, blocos de assinatura completos.
2. Se for título executivo extrajudicial (art. 784 CPC), verifica se precisa de duas testemunhas.
3. Escolhe o tipo de assinatura (simples / avançada / qualificada ICP-Brasil) conforme a matéria.
4. Configura o envelope: ordem (paralela ou sequencial), prazo, lembretes, observadores, autenticação adicional.
5. Após assinado, arquiva no CLM, armazenamento e sistema de gestão.

**Exemplo prático.** "Fechamos a negociação com o cliente sexta à tarde. Rodei `/solicitar-assinatura` com a minuta final. O plugin pegou que faltava anexar o Anexo II (SLA), que o representante do cliente aparecia como diretor mas a procuração no sistema estava vencida, e que a cláusula de foro ainda estava marcada como [CIDADE]. Corrigimos tudo antes de mandar o envelope — evitou retrabalho e constrangimento."

---

## 11. `/triar-nda` — Triagem de NDA

**O que é.** Classifica um Acordo de Confidencialidade recebido em **VERDE** (assina sob alçada delegada), **AMARELO** (precisa revisão de advogado antes) ou **VERMELHO** (precisa negociação ou revisão completa). Baseado em critérios objetivos.

**Quando acionar.**
- Chegou NDA de prospect, fornecedor, cliente, investidor.
- Área de negócio quer saber se pode assinar sozinha ou se tem que parar para revisão.

**Protocolo.**
1. Extrai do NDA: partes, mutualidade, definição de informação confidencial, prazo, carve-outs, penalidades, foro, cláusulas atípicas (non-solicit, non-compete, exclusividade).
2. Compara com o playbook do escritório.
3. Classifica:
   - **VERDE** — mútuo, prazo até 5 anos (ou indeterminado para segredo de indústria), carve-outs completos, sem non-solicit/non-compete, foro brasileiro ou arbitragem em câmara reconhecida, LGPD endereçada.
   - **AMARELO** — desvios contornáveis (prazo 5-10 anos, carve-outs incompletos, foro estranho, LGPD ausente).
   - **VERMELHO** — sinais sérios (non-compete, non-solicit disfarçado, prazo acima de 10 anos, penalidade desproporcional, contraparte em lista restritiva).
4. Entrega checklist, sugestões de ajuste e encaminhamento.

**Exemplo prático.** "Comercial mandou NDA do prospect às 16h de sexta com pressa para assinar. Rodei `/triar-nda`. Classificação: AMARELO. Motivo: sem carve-out para informação exigida por autoridade judicial, prazo de 7 anos, LGPD não endereçada apesar de haver troca de dados de funcionários na fase de diligência. O plugin entregou red-lines em três cláusulas. Avisei comercial, ajustamos, devolvemos para a contraparte na segunda — ganhamos dois dias e evitamos assinar algo problemático."

---

## 12. `/verificar-fornecedor` — Verificação de fornecedor

**O que é.** Consolida em um único lugar tudo o que o escritório/empresa tem com um fornecedor ou cliente específico: contratos (MSA, SOW, DPA, NDA), prazos, histórico, pendências, situação de compliance (certidões, cadastros negativos, listas restritivas).

**Quando acionar.**
- Homologação de novo fornecedor.
- Renovação de contrato existente.
- Antes de ampliar o relacionamento (novo produto, nova unidade).
- Revisão periódica de carteira de fornecedores críticos.

**Protocolo.**
1. Normaliza a identificação (razão social, CNPJ, grupo econômico, alterações societárias).
2. Varre CLM, armazenamento, e-mail, CRM, sistema de gestão para encontrar todos os documentos.
3. Lista lacunas: falta NDA? falta MSA? falta DPA (se há tratamento de dados pessoais)? procuração vigente? ato constitutivo atualizado?
4. Indica o que consultar nos portais oficiais: Receita Federal (situação CNPJ), CND Federal/Estadual/Municipal, FGTS, CNDT, CEIS, CNEP, SICAF (se fornece ao governo), listas OFAC (se há exposição internacional). O plugin **não presume** validade de certidão — só sinaliza que precisa consultar.
5. Lista prazos próximos, renovações automáticas, obrigações sobreviventes, pendências e recomendações.

**Exemplo prático.** "Área de suprimentos queria renovar contrato com fornecedor de software por mais 3 anos com aumento de escopo. Rodei `/verificar-fornecedor` com o CNPJ. O plugin mostrou que o MSA estava vigente, mas o DPA tinha vencido há 14 meses (o fornecedor passou a tratar dados de clientes finais desde o ano passado — lacuna crítica de LGPD), havia uma controvérsia de SLA aberta no sistema de tickets e o cadastro da empresa na Receita estava com pendência recente. Renegociamos com DPA atualizado antes de renovar."

---

## Como combinar skills

Muitas vezes você usa mais de uma skill em sequência. Alguns fluxos comuns:

**Análise processual completa.** `/analise-processo-medio` → `/avaliar-risco` para classificar o risco da condenação → `/reuniao-briefing` antes da AIJ.

**Onboarding de fornecedor.** `/verificar-fornecedor` para status atual → `/verificar-compliance` para mapear obrigações LGPD/Anticorrupção → `/revisar-contrato` na minuta → `/solicitar-assinatura` quando fechado.

**NDA recebido.** `/triar-nda` → se amarelo/vermelho, `/revisar-contrato` → quando fechado, `/solicitar-assinatura`.

**Incidente de dados.** `/brief incidente` para panorama → `/avaliar-risco` para classificar exposição → `/responder hold-documentos` para preservação → `/responder titular-dados` para eventuais comunicações aos titulares → `/verificar-compliance` para mapear reportes obrigatórios (ANPD, setorial, fato relevante CVM).

---

## O que o plugin nunca vai fazer

- **Nunca inventa jurisprudência, doutrina, súmula, enunciado ou precedente.** Se não está nos autos ou em fonte conectada, ele diz "não localizado" e recomenda pesquisa dedicada.
- **Nunca afirma fato processual sem base documental.** Cada afirmação tem referência à folha, ID ou documento de origem.
- **Nunca substitui o advogado.** Toda produção é minuta — precisa de revisão do profissional responsável antes de sair.
- **Nunca quebra sigilo.** Documentos analisados são tratados como matéria submetida a sigilo profissional (art. 7º, XIX, Lei 8.906/94).

---

## Boas práticas

Quando rodar uma skill, dê o máximo de contexto possível logo no início: objetivo, prazo, parte representada, foco temático. Quanto melhor o briefing, melhor o resultado.

Se o plugin pedir um dado que você não tem, ele vai deixar o campo como `[A PREENCHER]`. Preencha antes de enviar qualquer coisa para fora do escritório.

Para processos longos, o plugin preserva o índice entre sessões — você não precisa reprocessar tudo na segunda vez.

Quando envolve dados pessoais (próprios, de clientes, de titulares), lembre que o DPO precisa ser comunicado conforme a política interna.

Revise sempre. O plugin acelera o trabalho — não o dispensa.
