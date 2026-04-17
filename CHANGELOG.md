# Changelog

Todas as mudanças notáveis no Plugin Chiapetti Advogados estão documentadas neste arquivo.

Segue [Semantic Versioning](https://semver.org/).

---

## [0.1.0] - 2026-04-17

### Added
- Skill: `analise-processo` — Análise completa de processos judiciais
- Skill: `review-contract` — Review cláusula a cláusula com red-lines
- Skill: `triage-nda` — Triagem rápida de NDAs (VERDE/AMARELO/VERMELHO)
- Skill: `compliance-check` — Verificação de conformidade regulatória
- Skill: `legal-risk-assessment` — Matriz de severidade × probabilidade
- Skill: `meeting-briefing` — Briefing para reuniões com relevância jurídica
- Skill: `vendor-check` — Status de contratos e lacunas de documentação
- GitHub Actions workflow para versionamento automático
- Documentação completa e guias de uso

### Changed
- Nenhuma mudança nesta versão inicial

### Fixed
- Nenhuma correção nesta versão inicial

### Security
- Nenhuma mudança de segurança nesta versão inicial

---

## Template para Futuras Versões

Use este template quando criar novo release:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- Nova feature/skill

### Changed
- Feature modificada

### Fixed
- Bug corrigido

### Security
- Patch de segurança (se houver)

### Deprecated
- Funcionalidade que será removida em versão futura
```

---

## Como Versionar

### Leia antes de cada commit

1. **Nova funcionalidade**?
   ```bash
   git commit -m "feat: add support for labor law analysis"
   # Resultado: 0.1.0 → 0.2.0 (minor bump)
   ```

2. **Bug fix**?
   ```bash
   git commit -m "fix: correct contract date parsing logic"
   # Resultado: 0.1.0 → 0.1.1 (patch bump)
   ```

3. **Breaking change** (muda interface/contrato)?
   ```bash
   git commit -m "feat!: restructure risk assessment categories"
   # Resultado: 0.1.0 → 1.0.0 (major bump)
   ```

### GitHub Actions automatiza tudo

Após `git push origin main`:
1. ✓ Lê tipo de mudança do commit
2. ✓ Calcula nova versão
3. ✓ Atualiza arquivo `VERSION`
4. ✓ Cria git tag
5. ✓ Publica release no GitHub
6. ✓ Empacota plugin.zip

**Você não faz nada disso manualmente.**

---

## Histórico Completo

Ver releases: https://github.com/seu-usuario/chiapetti-plugin-legal/releases

Ver commits: https://github.com/seu-usuario/chiapetti-plugin-legal/commits/main

---

## Notas

- **Atualizações automáticas**: Claude puxa sempre a versão `latest` — sem ação manual
- **Rollback**: Se precisar reverter, use `git revert <hash>` + `git push` — nova release é criada automaticamente
- **Comunicação de mudanças**: Cada release gera automaticamente notas com commit message

---

**Mantido por**: Rodrigo Chiapetti | rodrigo@chiapettiadvogados.com.br
