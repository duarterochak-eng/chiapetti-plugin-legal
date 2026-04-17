# Setup: Versionamento Automático do Plugin Chiapetti Advogados

## 1. Criar Repositório GitHub

### Via web (GitHub.com)
1. Acesse https://github.com/new
2. Preencha:
   - **Repository name**: `chiapetti-plugin-legal`
   - **Description**: "Plugin Claude para análise jurídica e casos — Chiapetti Advogados"
   - **Public** (recomendado para auto-deploy simples) ou **Private** (se usar GitHub Pages com autenticação)
   - Marque: "Add a README file"
3. Clique "Create repository"

### Via CLI (se tiver Git instalado)
```bash
git init chiapetti-plugin-legal
cd chiapetti-plugin-legal
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/seu-usuario/chiapetti-plugin-legal.git
git branch -M main
git push -u origin main
```

## 2. Estrutura de Pasta (clone / clone e edite localmente)

```
chiapetti-plugin-legal/
├── .github/
│   └── workflows/
│       └── deploy.yml          # Auto-deploy via GitHub Actions
├── plugin/
│   ├── plugin.json             # Seu plugin.json
│   ├── SKILL.md                # Documentação da skill (se aplicável)
│   ├── skills/
│   │   ├── skill-1/
│   │   │   └── SKILL.md
│   │   └── skill-2/
│   │       └── SKILL.md
│   └── connectors/             # Se tiver conexões MCP/custom
│       └── example.json
├── docs/
│   ├── README.md               # Documentação principal
│   ├── CHANGELOG.md            # Histórico de versões
│   └── CONTRIBUTING.md         # Instruções para manutenção
├── .gitignore
├── README.md
└── VERSION                      # Arquivo com versão atual (ex: 1.0.0)
```

## 3. Criar arquivo `.github/workflows/deploy.yml`

Copie o arquivo `deploy.yml` fornecido neste pacote para `.github/workflows/deploy.yml`.

Este workflow:
- **Monitora mudanças** em qualquer push para `main`
- **Incrementa versão** automaticamente (major.minor.patch)
- **Atualiza VERSION** no repo
- **Publica release** no GitHub
- **Notifica** mudanças via webhook (opcional)

## 4. Adicionar Segredo GitHub (para notificações/deploy avançado)

Se quiser webhooks ou notificações:

1. Vá para: **Settings** → **Secrets and variables** → **Actions**
2. Clique "New repository secret"
3. Adicione (opcional):
   - `DEPLOY_WEBHOOK_URL`: Endpoint que receberá notificação de novo deploy
   - `GITHUB_TOKEN`: Auto-gerado pelo GitHub (não precisa adicionar)

## 5. Iniciar Versionamento

### Primeiro push com estrutura
```bash
# Clonar repo (se não tiver localmente)
git clone https://github.com/seu-usuario/chiapetti-plugin-legal.git
cd chiapetti-plugin-legal

# Adicionar arquivos do plugin
cp seu-plugin.json plugin/plugin.json
# ... copie skills e outros arquivos para pastas corretas

# Fazer commit
git add .
git commit -m "feat: add initial plugin structure with legal analysis skills"
git push origin main
```

**O GitHub Actions vai disparar automaticamente e:**
- Criar tag de versão (ex: `v0.1.0`)
- Empacotar plugin
- Criar release no GitHub

### Fluxo diário: editar e atualizar

Sempre que você editar arquivos do plugin:

```bash
git add .
git commit -m "feat: add new clause analysis skill"
# ou
git commit -m "fix: improve contract review logic"
# ou
git commit -m "docs: update legal risk assessment"

git push origin main
```

**Cada push = nova versão + release automático**

## 6. Consumir Plugin (URL para Claude)

Após o primeiro deploy, seu plugin está disponível em:

```
https://github.com/seu-usuario/chiapetti-plugin-legal/releases/latest/download/plugin.zip
```

Ou versão específica:
```
https://github.com/seu-usuario/chiapetti-plugin-legal/releases/download/v1.0.0/plugin.zip
```

**Claude sempre puxa a versão `latest`** — nenhuma ação manual necessária.

## 7. Monitorar Versões e Histórico

- **Releases**: https://github.com/seu-usuario/chiapetti-plugin-legal/releases
- **Commits**: https://github.com/seu-usuario/chiapetti-plugin-legal/commits/main
- **Tags**: `git tag -l` (local)

## Convenções de Commit (mantém changelog automático)

Use prefixos no seu commit para que o versionamento saiba como incrementar versão:

| Prefixo | Incremento | Exemplo |
|---------|-----------|---------|
| `feat:` | Minor (0.1.0 → 0.2.0) | `feat: add support for labor case analysis` |
| `fix:` | Patch (0.1.0 → 0.1.1) | `fix: correct risk assessment formula` |
| `docs:` | Patch | `docs: update NDA triage guide` |
| `BREAKING CHANGE:` | Major (0.1.0 → 1.0.0) | `feat!: restructure contract template format` |

---

## Próximos Passos

1. Crie repositório no GitHub
2. Clone para seu PC
3. Copie `deploy.yml` para `.github/workflows/`
4. Adicione seu plugin à pasta `/plugin`
5. Faça commit e push
6. Verifique Actions → Deploy foi bem-sucedido
7. Use a URL de release no Claude

**Suporte**: Se o workflow falhar, verifique a aba **Actions** no GitHub para logs de erro.
