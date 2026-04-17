# Guia Rápido: Git & GitHub Commands

## Instalação de Pré-requisitos

### Windows

1. **Git**: https://git-scm.com/download/win
   - Instale com configurações padrão
   - Restart do Windows após instalação

2. **GitHub Desktop** (opcional, alternativa visual):
   - https://desktop.github.com/

### macOS / Linux

```bash
# macOS (com Homebrew)
brew install git

# Ubuntu/Debian
sudo apt-get install git
```

## Configuração Inicial (primeira vez)

```bash
# Configurar nome e email globalmente
git config --global user.name "Rodrigo Chiapetti"
git config --global user.email "rodrigo@chiapettiadvogados.com.br"

# Verificar configuração
git config --list
```

## Fluxo Diário: Clone → Edit → Commit → Push

### 1. Clonar repositório (primeira vez)

```bash
git clone https://github.com/seu-usuario/chiapetti-plugin-legal.git
cd chiapetti-plugin-legal
```

### 2. Criar branch para sua mudança (opcional, boa prática)

```bash
git checkout -b feature/sua-mudanca
# Exemplo:
git checkout -b feature/add-labor-analysis
```

### 3. Editar arquivos

Use editor de sua escolha (VS Code, Notepad++, etc.)

Exemplo: Editar `plugin/skills/analise-processo/SKILL.md`

### 4. Verificar o que mudou

```bash
# Ver arquivos modificados
git status

# Ver diffs exatos
git diff plugin/skills/analise-processo/SKILL.md
```

### 5. Staged (preparar para commit)

```bash
# Adicionar arquivo específico
git add plugin/skills/analise-processo/SKILL.md

# Ou adicionar TODOS os arquivos modificados
git add .

# Verificar o que está staged
git status
```

### 6. Commit (salvar mudanças localmente)

```bash
# Formato: git commit -m "tipo: descrição"
git commit -m "feat: add labor law analysis to analise-processo"

# Exemplos:
git commit -m "fix: correct contract date parsing"
git commit -m "docs: update README with new features"
git commit -m "feat!: restructure risk assessment framework"

# Ver histórico local
git log --oneline -5
```

### 7. Push (enviar para GitHub)

```bash
# Se criou branch
git push origin feature/add-labor-analysis

# Se está em main
git push origin main

# Resultado: GitHub Actions dispara automaticamente!
```

## Ver Status do Deploy

1. Acesse: https://github.com/seu-usuario/chiapetti-plugin-legal
2. Clique em **Actions**
3. Veja workflow **Auto-Deploy Plugin** rodando
4. Após sucesso, novo release aparece em **Releases**

## Comandos Úteis

### Ver histórico

```bash
# Últimos 10 commits
git log --oneline -10

# Commits de um arquivo específico
git log --oneline plugin/skills/analise-processo/SKILL.md

# Gráfico visual
git log --graph --oneline --all --decorate
```

### Ver tags (versões)

```bash
# Listar todas as tags
git tag -l

# Ver detalhes de uma tag
git show v0.2.0

# Criar tag local (raro — GitHub Actions faz isso)
git tag -a v0.2.0 -m "Release version 0.2.0"
```

### Desfazer mudanças

```bash
# Desfazer edição de arquivo (antes de git add)
git checkout -- plugin/skills/analise-processo/SKILL.md

# Remover commit local (antes de push)
git reset --soft HEAD~1

# Reverter commit já feito (cria novo commit)
git revert <hash-do-commit>
git push origin main
```

### Sincronizar com remoto

```bash
# Puxar mudanças do GitHub (raro, você é o único editor)
git pull origin main

# Forçar sincronização (descarta mudanças locais)
git fetch origin
git reset --hard origin/main
```

## Cenários Comuns

### Cenário 1: Adicionar nova skill

```bash
# Criar branch
git checkout -b feature/nova-skill-analise

# Editar: criar plugin/skills/sua-skill/SKILL.md

# Adicionar e commitar
git add plugin/skills/sua-skill/
git commit -m "feat: add new skill for labor law analysis"

# Push
git push origin feature/nova-skill-analise

# Criar Pull Request (opcional) ou
# Fazer merge manual para main:
git checkout main
git merge feature/nova-skill-analise
git push origin main
```

### Cenário 2: Corrigir bug em skill existente

```bash
# Editar arquivo da skill
# Ex: plugin/skills/review-contract/SKILL.md

# Adicionar e commitar (direto para main é ok para bugs)
git add plugin/skills/review-contract/SKILL.md
git commit -m "fix: correct contract clause detection regex"

# Push
git push origin main
```

### Cenário 3: Atualizar documentação

```bash
git add docs/ README_PLUGIN.md
git commit -m "docs: clarify risk assessment methodology"
git push origin main
```

## Troubleshooting

### "fatal: not a git repository"

Você não está dentro da pasta do repositório.

```bash
cd caminho/para/chiapetti-plugin-legal
```

### "nothing to commit, working tree clean"

Sem mudanças detectadas. Verifique se editou o arquivo e salvou.

```bash
git status  # Confirmar
```

### "Your branch is ahead of 'origin/main' by 1 commit"

Você fez commit mas não fez push ainda.

```bash
git push origin main
```

### Merge conflicts

Se múltiplas pessoas editarem mesmo arquivo (raro aqui):

```bash
# Abrir arquivo, resolver conflitos manualmente
# Procurar por: <<<<<<< ======= >>>>>>>

git add arquivo-resolvido
git commit -m "fix: resolve merge conflict"
git push origin main
```

## Recursos Úteis

- **Git Cheat Sheet**: https://github.github.com/training-kit/downloads/github-git-cheat-sheet.pdf
- **Interactive Tutorial**: https://learngitbranching.js.org/
- **GitHub Docs**: https://docs.github.com/

---

**Dúvida?** Contacte: rodrigo@chiapettiadvogados.com.br
