# Plugin Chiapetti Advogados — Análise Jurídica

Plugin Claude especializado em análise de processos, contratos, pareceres e questões de conformidade jurídica. Atualiza automaticamente cada vez que novos recursos são adicionados ou modificados.

## Versão Atual

```
v0.1.0
```

Ver histórico completo: [Releases](https://github.com/seu-usuario/chiapetti-plugin-legal/releases)

## Features

- **Análise de Processos**: Petições iniciais, decisões, recursos
- **Review de Contratos**: Identificação de desvios, sugestões de redação (red-lines)
- **Triage de NDAs**: Classificação rápida (VERDE/AMARELO/VERMELHO)
- **Verificação de Conformidade**: LGPD, regulação setorial, legislação aplicável
- **Risk Assessment**: Matriz de severidade × probabilidade com critérios de escalação
- **Briefings**: Preparação para reuniões com relevância jurídica
- **Vendor Check**: Status de acordos existentes, lacunas de documentação

## Instalação

### No Claude Cowork

1. Abra Claude Cowork
2. Vá para **Plugins** → **Install from URL**
3. Cole:
   ```
   https://github.com/seu-usuario/chiapetti-plugin-legal/releases/latest/download/plugin.zip
   ```
4. Clique "Install"

**O plugin se atualizará automaticamente** cada vez que houver novo release no GitHub.

## Estrutura do Plugin

```
plugin/
├── plugin.json              # Metadados do plugin
├── SKILL.md                 # Documentação principal
└── skills/
    ├── analise-processo/
    │   └── SKILL.md
    ├── review-contract/
    │   └── SKILL.md
    ├── triage-nda/
    │   └── SKILL.md
    ├── compliance-check/
    │   └── SKILL.md
    └── ... (outras skills)
```

## Como Atualizar o Plugin

### Adicionar Nova Skill

1. Crie pasta em `plugin/skills/sua-skill/`
2. Adicione arquivo `SKILL.md` com documentação
3. Edite `plugin/plugin.json` se necessário
4. Faça commit:
   ```bash
   git add plugin/
   git commit -m "feat: add new skill for assessment"
   git push origin main
   ```
5. **Pronto!** GitHub Actions dispara automaticamente, incrementa versão e publica.

### Corrigir Bug em Skill Existente

```bash
# Edite o arquivo da skill
# Ex: plugin/skills/analise-processo/SKILL.md

git add plugin/skills/analise-processo/SKILL.md
git commit -m "fix: correct risk assessment calculation in analise-processo"
git push origin main
```

**Versão é incrementada automaticamente** (patch bump: 0.1.0 → 0.1.1)

### Mudança Drástica (quebra compatibilidade)

```bash
git commit -m "feat!: restructure contract template format"
# ou
git commit -m "BREAKING CHANGE: refactor NDA triage categories"
git push origin main
```

**Versão salta major**: 0.1.0 → 1.0.0

## Convenções de Commit

Use prefixos padronizados — o workflow GitHub Action usa isso para versionar:

| Prefixo | Significado | Novo Versão |
|---------|-----------|-----------|
| `feat:` | Nova feature | 0.1.0 → 0.2.0 (minor) |
| `fix:` | Bug fix | 0.1.0 → 0.1.1 (patch) |
| `docs:` | Apenas documentação | 0.1.0 → 0.1.1 (patch) |
| `feat!:` ou `BREAKING CHANGE:` | Muda interface/contrato | 0.1.0 → 1.0.0 (major) |
| `chore:` | Limpeza/config (sem release) | sem mudança |

## Versionamento Semântico

Plugin segue [SemVer](https://semver.org/):

- **MAJOR** (1.0.0): Mudanças incompatíveis (breaking changes)
- **MINOR** (0.2.0): Nova feature compatível
- **PATCH** (0.1.1): Bug fixes

## Monitorar Versões

### Via GitHub

- **Releases**: https://github.com/seu-usuario/chiapetti-plugin-legal/releases
- **Commits**: https://github.com/seu-usuario/chiapetti-plugin-legal/commits/main
- **Tags**: https://github.com/seu-usuario/chiapetti-plugin-legal/tags

### Via linha de comando (Git)

```bash
git log --oneline        # Ver histórico de commits
git tag -l              # Ver todas as versões/tags
git show v0.2.0         # Detalhes de uma versão específica
```

## Troubleshooting

### Deploy falhou

1. Verifique **Actions** no GitHub para logs de erro
2. Comum: `plugin.json` inválido — valide JSON
3. Confirme estrutura: arquivo obrigatório `plugin/plugin.json` existe?

### Plugin não atualiza no Claude

- Reinstale a partir do URL latest:
  ```
  https://github.com/seu-usuario/chiapetti-plugin-legal/releases/latest/download/plugin.zip
  ```
- Ou espere ~5min para cache do GitHub atualizar

### Reverter para versão anterior

```bash
git revert <commit-hash>
git push origin main
# Novo release será criado automaticamente
```

## Contato

Para sugestões ou reportar issues:
1. Abra issue no GitHub: https://github.com/seu-usuario/chiapetti-plugin-legal/issues
2. Ou contacte: rodrigo@chiapettiadvogados.com.br

---

**Atualizado**: v0.1.0 | **Próxima release**: Automática a cada mudança
