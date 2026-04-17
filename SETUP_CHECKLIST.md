# ✓ Setup Checklist: Plugin com Auto-Deploy

Siga este checklist **uma única vez** para configurar o sistema. Depois, basta editar e fazer `git push`.

---

## Fase 1: GitHub (Criar Repositório)

- [ ] **1.1** Acesse https://github.com/new
- [ ] **1.2** Preencha:
  - Repository name: `chiapetti-plugin-legal`
  - Description: "Plugin Claude para análise jurídica — Chiapetti Advogados"
  - Visibility: **Public** (simplifica auto-deploy) *ou* Private (se tiver conhecimento de OAuth)
  - Check: "Add a README file"
- [ ] **1.3** Clique "Create repository"
- [ ] **1.4** Copie URL do repo: `https://github.com/seu-usuario/chiapetti-plugin-legal.git`

---

## Fase 2: Git Local (Setup no seu PC)

### 2.1 Instalar Git (se não tiver)

- [ ] Baixe https://git-scm.com/download/win (Windows)
- [ ] Instale com configurações padrão
- [ ] Restart do Windows

### 2.2 Configurar Git

- [ ] Abra PowerShell ou Terminal
- [ ] Execute:
  ```bash
  git config --global user.name "Rodrigo Chiapetti"
  git config --global user.email "rodrigo@chiapettiadvogados.com.br"
  git config --list  # Verificar
  ```

### 2.3 Clonar Repositório

- [ ] Escolha pasta local (ex: `C:\Users\seu-usuario\Documentos`)
- [ ] Abra PowerShell nessa pasta
- [ ] Execute:
  ```bash
  git clone https://github.com/seu-usuario/chiapetti-plugin-legal.git
  cd chiapetti-plugin-legal
  ```

---

## Fase 3: Estrutura de Pastas (Copiar Arquivos)

- [ ] **3.1** Crie estrutura:
  ```
  chiapetti-plugin-legal/
  ├── .github/
  │   └── workflows/
  │       └── deploy.yml          (copiar arquivo deploy.yml aqui)
  ├── plugin/
  │   ├── plugin.json             (seu plugin.json)
  │   └── skills/
  │       └── ... (suas skills)
  ├── docs/
  ├── .gitignore                  (copiar arquivo .gitignore aqui)
  ├── VERSION                      (criar arquivo com: 0.1.0)
  ├── README.md                    (copiar README_PLUGIN.md aqui)
  └── CHANGELOG.md                 (copiar CHANGELOG.md aqui)
  ```

- [ ] **3.2** Copie os arquivos fornecidos:
  - [ ] `deploy.yml` → `.github/workflows/deploy.yml`
  - [ ] `.gitignore` → `.gitignore` (raiz)
  - [ ] `README_PLUGIN.md` → `README.md` (raiz)
  - [ ] `CHANGELOG.md` → `CHANGELOG.md` (raiz)

- [ ] **3.3** Crie arquivo `VERSION` na raiz:
  ```
  Conteúdo: 0.1.0
  ```

---

## Fase 4: Adicionar Seu Plugin

- [ ] **4.1** Copie seu `plugin.json` para `plugin/plugin.json`

- [ ] **4.2** Organize suas skills em `plugin/skills/`:
  ```
  plugin/skills/
  ├── analise-processo/
  │   └── SKILL.md
  ├── review-contract/
  │   └── SKILL.md
  └── ... (outras skills)
  ```

  *Referência: Ver `DIRECTORY_STRUCTURE.txt` para estrutura detalhada*

- [ ] **4.3** Valide `plugin.json`:
  - Abra https://jsonlint.com/
  - Cole conteúdo de `plugin/plugin.json`
  - Verifique se não há erros

---

## Fase 5: Primeiro Commit & Push

- [ ] **5.1** No PowerShell, dentro da pasta do repo:
  ```bash
  git status  # Verificar arquivos
  ```

- [ ] **5.2** Adicionar tudo:
  ```bash
  git add .
  ```

- [ ] **5.3** Primeiro commit:
  ```bash
  git commit -m "feat: initialize plugin with legal analysis skills"
  ```

- [ ] **5.4** Push para GitHub:
  ```bash
  git push origin main
  ```

---

## Fase 6: Verificar Deploy Automático

- [ ] **6.1** Acesse GitHub repo: https://github.com/seu-usuario/chiapetti-plugin-legal

- [ ] **6.2** Clique em **Actions** (aba no topo)

- [ ] **6.3** Veja workflow **Auto-Deploy Plugin** rodando

- [ ] **6.4** Aguarde conclusão (1-2 min)

- [ ] **6.5** Clique em **Releases** (aba no topo)

- [ ] **6.6** Verifique se novo release `v0.1.0` apareceu com arquivo `plugin-v0.1.0.zip`

---

## Fase 7: Configurar no Claude

- [ ] **7.1** Abra Claude Cowork

- [ ] **7.2** Vá para **Plugins** → **Install from URL**

- [ ] **7.3** Cole a URL:
  ```
  https://github.com/seu-usuario/chiapetti-plugin-legal/releases/latest/download/plugin.zip
  ```

- [ ] **7.4** Clique "Install"

- [ ] **7.5** Aguarde instalação concluir

- [ ] **7.6** Verifique se plugin aparece em lista

---

## Fase 8: Testar Atualização Automática

- [ ] **8.1** Edite um arquivo do plugin localmente (ex: `plugin/plugin.json`)

- [ ] **8.2** Salve arquivo

- [ ] **8.3** No PowerShell:
  ```bash
  git add .
  git commit -m "fix: test auto-update mechanism"
  git push origin main
  ```

- [ ] **8.4** Aguarde 1-2 min

- [ ] **8.5** Verifique **Releases** no GitHub — nova versão deve aparecer (v0.1.1)

- [ ] **8.6** No Claude, próxima inicialização, plugin se atualiza automaticamente

---

## ✓ Pronto!

Você configurou com sucesso:
- ✓ Repositório Git versionado
- ✓ GitHub Actions auto-deploy
- ✓ Plugin disponível no Claude com updates automáticos

### Daqui em diante:

```bash
# 1. Edite arquivo do plugin
# 2. git add .
# 3. git commit -m "sua mensagem"
# 4. git push origin main
# 5. ✓ Deploy automático dispara
# 6. ✓ Claude puxa versão latest na próxima inicialização
```

---

## Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| "fatal: not a git repository" | Use `cd caminho/chiapetti-plugin-legal` antes de rodar comandos |
| Deploy falha no GitHub Actions | Verifique **Actions** → logs. Comum: `plugin.json` com erro JSON |
| Plugin não atualiza no Claude | Aguarde 5min. Ou reinstale URL em **Plugins** → **Manage** |
| "Your branch is ahead..." | Você fez commit mas não push. Rode `git push origin main` |
| Arquivo `VERSION` não existe | Crie manualmente: novo arquivo, conteúdo `0.1.0` |

---

## Próximos Passos

- Leia `QUICK_CLI_GUIDE.md` para dominar Git
- Consulte `DIRECTORY_STRUCTURE.txt` para organizar skills
- Veja `README_PLUGIN.md` para documentação de uso

---

**Concluído?** Parabéns! Seu plugin agora tem versionamento e deploy automático. 🎉

Dúvidas: rodrigo@chiapettiadvogados.com.br
