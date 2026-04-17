# Plugin Jurídico (PT-BR / Brasil)

Plugin de produtividade para advogados brasileiros, adaptado integralmente ao ordenamento jurídico nacional. Automatiza análise processual (pequena, média e de grande volume — 1000+ páginas), revisão de contratos, triagem de NDAs, rotinas de compliance (LGPD, CDC, Lei Anticorrupção, Lei das S.A.), elaboração de pareceres, briefings e respostas templatizadas.

> **Aviso.** Este plugin é ferramenta de apoio ao trabalho jurídico e **não substitui** o juízo técnico do advogado inscrito na OAB. Toda produção deve ser revisada pelo profissional responsável. O plugin respeita integralmente o Código de Ética e Disciplina da OAB e o Provimento 205/2021 do Conselho Federal da OAB (uso de IA na advocacia).

## Diretriz inegociável: vedação à alucinação

**A IA jamais fantasiará, inventará ou presumirá informação sem base documental.** Em particular:

- **Nunca** citará jurisprudência, doutrina, dispositivo legal, súmula, enunciado ou precedente que não tenha sido fornecido nos autos/documentos ou recuperado por fonte conectada verificável.
- **Nunca** afirmará fatos processuais que não estejam comprovados nos documentos analisados.
- **Sempre** distinguirá entre (i) o que consta nos autos, (ii) o que é fundamento legal objetivo (com indicação do dispositivo) e (iii) o que é inferência ou hipótese analítica — esta última sempre rotulada como tal.
- **Diante de lacuna**, declarará expressamente "informação não encontrada nos documentos/fontes disponíveis" em vez de presumir.
- **Tom sempre formal, técnico e sério.** Nenhuma especulação narrativa, analogia literária ou linguagem informal. Terminologia jurídica precisa em PT-BR.

## Público-alvo

Advogados autônomos, escritórios de advocacia e departamentos jurídicos internos atuando no Brasil, em qualquer área: cível, trabalhista, tributária, empresarial, consumerista, administrativa, penal empresarial, regulatório, proteção de dados, entre outras.

## Instalação

```
claude plugins add legal-br
```

## Configuração do playbook local

Crie um arquivo `legal.local.md` na pasta conectada ao Cowork (ou em `.claude/` no Claude Code) para codificar as posições-padrão do escritório, incluindo foro preferencial, teses recorrentes, posições contratuais padrão, requisitos de DPA sob LGPD, padrões de NDA e caminhos para templates de peças.

## Conecte suas ferramentas

O plugin funciona melhor conectado às ferramentas existentes via MCP: Gmail, Microsoft 365, Google Calendar, Google Drive, Atlassian. Consulte [CONNECTORS.md](CONNECTORS.md).

## Comandos (skills)

### Análise processual — escalonada por volume

| Comando | Faixa | Uso |
|---------|-------|-----|
| `/analise-processo-pequeno` | até ~100 páginas | Petições isoladas, JEC, processos iniciais, análise pontual de peça |
| `/analise-processo-medio` | ~100 a 1000 páginas | Processos em trâmite ordinário, volume médio de provas e decisões |
| `/analise-processo-extenso` | **1000+ páginas** | Processos de massa, recuperações judiciais, ações coletivas, autos robustos — estratégia de chunking, indexação e sumarização hierárquica |

### Demais comandos

| Comando | Função |
|---------|--------|
| `/brief` | Briefing diário, por tema, ou de incidente jurídico |
| `/revisar-contrato` | Revisão contratual cláusula a cláusula contra o playbook |
| `/triar-nda` | Triagem rápida de NDA — VERDE, AMARELO, VERMELHO |
| `/verificar-fornecedor` | Status de contratos com um fornecedor/cliente (MSA, DPA, NDA, vigências) |
| `/avaliar-risco` | Classificação de risco (severidade × probabilidade) |
| `/responder` | Geração de resposta templatizada (titular de dados LGPD, hold de documentos, NDA, etc.) |
| `/verificar-compliance` | Checagem de aderência regulatória (LGPD, CDC, Anticorrupção, regulação setorial) |
| `/solicitar-assinatura` | Checklist pré-assinatura e roteamento (ICP-Brasil ou plataformas — Clicksign, D4Sign, ZapSign, DocuSign) |
| `/reuniao-briefing` | Preparação estruturada de reunião jurídica e acompanhamento de ações |

## Arcabouço legal de referência

Referências reiteradas nos fluxos do plugin (não exaustivo):

**Processual**: CF/88 (art. 5º, LIV, LV); CPC/2015 (Lei 13.105/2015); Lei 9.099/95 (JECs); CPP; CLT (arts. 763-910); Lei 13.467/2017; Resoluções CNJ 345/2020 (Juízo 100% Digital) e 385/2021.

**Material**: CC/2002; CDC (Lei 8.078/90); CLT; Lei das S.A. (6.404/76); Lei 11.101/2005 (Recuperação e Falência); Lei 10.406/2002; Marco Civil da Internet (12.965/2014); LGPD (13.709/2018); Lei Anticorrupção (12.846/2013); Lei 9.279/96 (PI); Lei 9.307/96 (Arbitragem); Lei 14.133/2021 (Licitações); Lei 6.015/73 (Registros Públicos).

**Tributário**: CTN (Lei 5.172/66); LC 123/2006; LC 87/96; Lei 9.430/96; normativas da RFB.

**Regulatório específico**: conforme setor — BACEN/CVM/SUSEP (financeiro); ANS (saúde suplementar); ANATEL; ANEEL; ANVISA; ANTT/ANAC; CADE (concorrencial).

## Integração MCP

Configure em `.mcp.json`. O plugin degrada graciosamente quando uma ferramenta não está disponível — sinaliza lacunas e sugere verificações manuais.
