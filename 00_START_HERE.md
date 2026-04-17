# 🚀 Plugin Chiapetti: Sistema Completo de Versionamento & Auto-Deploy

Criou tudo que você precisa para hospedar seu plugin do Claude com **atualização automática a cada mudança**.

---

## O Que Você Conseguiu

✓ **Repositório GitHub** com versionamento automático  
✓ **GitHub Actions** que dispara deploy a cada `git push`  
✓ **Sem custos**: Usa GitHub Pages + releases (ambos gratuitos)  
✓ **Sem ação manual**: Cada commit = novo release automático  
✓ **Documentação completa**: Guias, checklists, exemplos  

---

## 📋 Ordem de Leitura (Comece Aqui)

### Primeira Vez: Setup (30-45 min)

1. **`SETUP_CHECKLIST.md`** ← **COMECE AQUI**
   - Checklist visual passo a passo
   - Cria GitHub repo
   - Configura Git local
   - Primeiro deploy

2. **`DIRECTORY_STRUCTURE.txt`** (enquanto segue checklist)
   - Visualização da estrutura de pastas
   - Onde copiar cada arquivo

### Depois: Uso Diário (5 min por mudança)

3. **`QUICK_CLI_GUIDE.md`** ← Domine Git
   - Comandos essenciais
   - Cenários comuns (adicionar skill, corrigir bug)
   - Troubleshooting rápido

### Referência Contínua

4. **`README_PLUGIN.md`** ← Documentação do plugin
   - Features disponíveis
   - Como instalar no Claude
   - Como atualizar

5. **`CHANGELOG.md`** ← Histórico de versões
   - Segue SemVer (0.1.0 → 0.2.0 → 1.0.0)
   - Auto-gerado pelo GitHub Actions

---

## 📦 Arquivos Fornecidos (Copie para seu Repo)

| Arquivo | Destino | Função |
|---------|---------|--------|
| `deploy.yml` | `.github/workflows/deploy.yml` | GitHub Actions workflow (coração do auto-deploy) |
| `.gitignore` | `.gitignore` (raiz) | Ignora arquivos temporários |
| `README_PLUGIN.md` | `README.md` (raiz) | Documentação principal |
| `CHANGELOG.md` | `CHANGELOG.md` (raiz) | Histórico de versões |
| (Crie) `VERSION` | `VERSION` (raiz) | Arquivo com versão (ex: 0.1.0) |

---

## 🎯 Fluxo Rápido (Dia a Dia)

### Setup Inicial (Uma Vez)

```bash
# 1. Clonar repo do GitHub
git clone https://github.com/seu-usuario/chiapetti-plugin-legal.git
cd chiapetti-plugin-legal

# 2. Copiar arquivos fornecidos para estrutura correta
# (Veja SETUP_CHECKLIST.md)

# 3. Primeiro push
git add .
git commit -m "feat: initialize plugin"
git push origin main

# 4. ✓ GitHub Actions dispara automático
# 5. ✓ Release v0.1.0 criado
```

### Fluxo Diário (Adicionar/Corrigir)

```bash
# 1. Edite arquivo do plugin
# 2. Salve

# 3. Git: preparar e enviar
git add .
git commit -m "feat: add new contract analysis"
git push origin main

# ✓ Pronto! Deploy automático dispara, versão muda para 0.2.0
# ✓ Claude puxa nova versão na próxima inicialização (sem você fazer nada)
```

---

## 🔧 Infraestrutura: Como Funciona

### Ciclo Automático

```
Local (seu PC)
  ↓ (git push)
GitHub Repository
  ↓ (webhook automático)
GitHub Actions (deploy.yml)
  ├─ Valida plugin.json
  ├─ Calcula versão (feat/fix/docs → bump type)
  ├─ Atualiza arquivo VERSION
  ├─ Cria git tag (ex: v0.2.0)
  ├─ Empacota plugin.zip
  └─ Publica Release
  ↓
GitHub Releases
  (URL: .../releases/latest/download/plugin.zip)
  ↓
Claude Cowork (você instalou URL única)
  ↓ (próxima inicialização)
Claude puxa versão latest automaticamente
```

**Você não faz nada depois do `git push`. Tudo é automático.**

---

## 💡 Convenções de Commit (Importante)

Use prefixos no seu commit — o GitHub Actions usa para versionar:

```bash
# Nova feature → incrementa MINOR (0.1.0 → 0.2.0)
git commit -m "feat: add labor law analysis skill"

# Bug fix → incrementa PATCH (0.1.0 → 0.1.1)
git commit -m "fix: correct contract date parsing"

# Apenas docs → incrementa PATCH
git commit -m "docs: clarify risk assessment methodology"

# BREAKING CHANGE → incrementa MAJOR (0.1.0 → 1.0.0)
git commit -m "feat!: restructure contract categories"
```

---

## 📂 Estrutura de Pastas (Resumen)

```
chiapetti-plugin-legal/
├── .github/workflows/deploy.yml    ← Auto-deploy (copiar)
├── plugin/
│   ├── plugin.json                 ← Seu plugin metadata
│   └── skills/
│       ├── analise-processo/SKILL.md
│       ├── review-contract/SKILL.md
│       └── ... (suas skills)
├── .gitignore                      ← (copiar)
├── VERSION                         ← Crie: 0.1.0
├── README.md                       ← (copiar README_PLUGIN.md)
└── CHANGELOG.md                    ← (copiar)
```

Detalhes: Veja `DIRECTORY_STRUCTURE.txt`

---

## ✅ Checklist Rápido

- [ ] Criei repositório GitHub `chiapetti-plugin-legal`
- [ ] Instalei Git e configurei (nome/email)
- [ ] Clonei repositório para PC
- [ ] Copiei arquivos fornecidos para estrutura correta
- [ ] Organizei meu plugin em `plugin/` com `plugin.json` e `skills/`
- [ ] Fiz primeiro commit: `git commit -m "feat: initialize plugin"`
- [ ] Fiz primeiro push: `git push origin main`
- [ ] Verifiquei GitHub Actions em **Actions** tab (deve estar rodando)
- [ ] Verifiquei Release criada em **Releases** tab
- [ ] Instalei plugin no Claude com URL: `https://github.com/.../releases/latest/download/plugin.zip`
- [ ] Testei atualização: editei arquivo, fiz push, verificou novo release
- [ ] ✓ Plugin atualiza automaticamente no Claude na próxima inicialização

---

## 🆘 Dúvidas Comuns

**P: Preciso fazer upload a cada mudança?**
A: Não. Cada `git push` = novo release automático no GitHub. Claude puxa versão latest.

**P: Preciso pagar por hosting?**
A: Não. GitHub e GitHub Actions são gratuitos. Releases também.

**P: Quanto tempo leva para atualizar?**
A: GitHub Actions: 1-2 min. Claude: próxima inicialização (com cache de ~5min).

**P: Como reverto uma mudança?**
A: `git revert <hash>` + `git push`. Novo release é criado automaticamente.

**P: Posso editar pelo GitHub web?**
A: Sim, mas recomendado editar localmente. GitHub web é para emergências.

---

## 📚 Referência Rápida: Próximos Arquivos a Ler

- **CLI não é seu forte?** → Leia `QUICK_CLI_GUIDE.md`
- **Estrutura confusa?** → Leia `DIRECTORY_STRUCTURE.txt`
- **Setup está travado?** → Leia `SETUP_CHECKLIST.md` de novo + `QUICK_CLI_GUIDE.md` seção Troubleshooting
- **Deploy falhou?** → GitHub Actions logs em **Actions** tab + `QUICK_CLI_GUIDE.md` troubleshooting

---

## 🎯 Próximos Passos

1. **Leia** `SETUP_CHECKLIST.md` (ordem exata)
2. **Execute** cada passo do checklist
3. **Verifique** GitHub Actions rodando
4. **Instale** no Claude com URL latest
5. **Teste** editando um arquivo e fazendo push
6. **Mantenha** usando `QUICK_CLI_GUIDE.md` diariamente

---

## 📞 Suporte

- **GitHub não está funcionando?** Procure logs em **Settings** → **Actions**
- **Git não está instalado?** Baixe https://git-scm.com/
- **Dúvida específica?** Verifique `QUICK_CLI_GUIDE.md` seção Troubleshooting

---

**Está tudo pronto. Comece por `SETUP_CHECKLIST.md`. Boa sorte! 🚀**

---

## Sumário: Arquivos Neste Pacote

| Arquivo | Tipo | Próposito |
|---------|------|---------|
| `00_START_HERE.md` | Guia | ← Você está aqui |
| `SETUP_CHECKLIST.md` | Checklist | Passo a passo setup (COMECE AQUI depois) |
| `QUICK_CLI_GUIDE.md` | Referência | Comandos Git e cenários comuns |
| `DIRECTORY_STRUCTURE.txt` | Referência | Estrutura de pastas visual |
| `SETUP_GITHUB.md` | Guia | Detalhes sobre GitHub setup |
| `deploy.yml` | Código | **COPIAR para `.github/workflows/`** |
| `.gitignore` | Código | **COPIAR para raiz** |
| `README_PLUGIN.md` | Documentação | **COPIAR para `README.md`** |
| `CHANGELOG.md` | Documentação | **COPIAR para raiz** |
| `plugin.json` | Referência | Seu arquivo (não é exemplo) |

---

**Pronto? Abra `SETUP_CHECKLIST.md` agora!**
