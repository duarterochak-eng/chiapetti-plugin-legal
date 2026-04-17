# Conectores

## Como as referências a ferramentas funcionam

Os arquivos do plugin utilizam `~~categoria` como marcador para indicar qualquer ferramenta que o usuário conecte naquela categoria. Por exemplo, `~~armazenamento` pode representar Google Drive, OneDrive, Box, Dropbox ou SharePoint.

Os plugins são **agnósticos quanto à ferramenta** — descrevem fluxos em termos de categorias (armazenamento, chat, e-mail, suíte de escritório, etc.) em vez de produtos específicos. O `.mcp.json` pré-configura alguns servidores MCP, mas qualquer servidor MCP daquela categoria funciona.

## Conectores deste plugin

| Categoria | Placeholder | Servidores incluídos | Outras opções |
|-----------|-------------|----------------------|---------------|
| Agenda | `~~agenda` | Google Calendar, Microsoft 365 | — |
| Chat | `~~chat` | — | Slack, Microsoft Teams |
| Armazenamento em nuvem | `~~armazenamento` | Google Drive | OneDrive, Dropbox, Box, SharePoint |
| CLM | `~~CLM` | — | DocuSign CLM, Ironclad, Conga |
| CRM | `~~CRM` | — | Salesforce, HubSpot, Pipedrive |
| E-mail | `~~email` | Gmail, Microsoft 365 | — |
| Assinatura eletrônica | `~~assinatura` | — | DocuSign, Clicksign, D4Sign, ZapSign, Adobe Sign |
| Suíte de escritório | `~~suíte` | Microsoft 365 | Google Workspace |
| Gestão de tarefas | `~~gestão` | Atlassian (Jira/Confluence) | Asana, Trello, Monday |
| PJe / e-SAJ / Projudi | `~~tribunal` | — | Integrações próprias via MCP (quando disponíveis) |

## Padrões brasileiros reconhecidos

Quando presentes nos conectores, os seguintes padrões/ferramentas típicas do mercado jurídico brasileiro são tratados de forma nativa: **Clicksign, D4Sign, ZapSign** (assinatura); **PJe, e-SAJ, Projudi, Eproc** (tribunais); **Legal One, CP-Pro, Projuris, Astrea** (gestão de processos/escritório); **Serpro/Datajud** (dados processuais públicos).
