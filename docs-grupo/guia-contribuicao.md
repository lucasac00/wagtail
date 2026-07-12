# Guia de Contribuição e Entrega — Grupo 03 — ES2 2026

**Sistema escolhido:** [Wagtail CMS](https://github.com/wagtail/wagtail)
**Fork do grupo:** [lucasac00/wagtail](https://github.com/lucasac00/wagtail)

---

## Integrantes

- Lucas Cardoso
- Arthur
- Samuel
- Júlia
- Luisa

---

## 1. Configuração inicial do ambiente

Cada membro deve clonar o fork do grupo e configurar os remotes:

```bash
git clone git@github.com:lucasac00/wagtail.git
cd wagtail
git remote add upstream git@github.com:wagtail/wagtail.git
```

Verifique se os remotes estão corretos:

```bash
git remote -v
# origin    git@github.com:lucasac00/wagtail.git (fetch/push)
# upstream  git@github.com:wagtail/wagtail.git (fetch/push)
```

### Build e execução local

Siga o guia `BUILD_AND_TEST_pt-br.md` na raiz do repositório. Resumo rápido:

```bash
python -m venv .venv && source .venv/bin/activate
sudo apt-get install libjpeg-dev zlib1g-dev
fnm install
pip install -e ".[testing,docs]"
npm ci && npm run build
DATABASE_NAME=wagtail_local.db DJANGO_SETTINGS_MODULE=wagtail.test.settings python wagtail/test/manage.py migrate
DATABASE_NAME=wagtail_local.db DJANGO_SETTINGS_MODULE=wagtail.test.settings python wagtail/test/manage.py createcachetable
DATABASE_NAME=wagtail_local.db DJANGO_SETTINGS_MODULE=wagtail.test.settings python wagtail/test/manage.py createsuperuser
DATABASE_NAME=wagtail_local.db DJANGO_SETTINGS_MODULE=wagtail.test.settings DJANGO_DEBUG=true python wagtail/test/manage.py runserver
```

---

## 2. Fluxo de trabalho com branches

### Estrutura de branches

```
upstream/main (wagtail/wagtail original)
     │
     ├── origin/main (fork do grupo) = upstream/main + pasta videos/ + docs-grupo/ + CI/SonarQube + código
     │
     ├── feature/nome-da-tarefa   ← branches de trabalho
     ├── fix/nome-do-fix
     │
     └── pr-upstream (branch temporária) → PR limpo para wagtail/wagtail
```

### Rotina diária

```bash
# 1. Atualize seu main com o upstream
git checkout main
git fetch upstream
git merge upstream/main
git push origin main

# 2. Crie uma branch para sua tarefa
git checkout -b feature/minha-tarefa

# 3. Faça as alterações, commits...

# 4. Envie para o fork
git push -u origin feature/minha-tarefa
```

### Abrindo um Pull Request interno

No GitHub, abra um PR de `feature/minha-tarefa` para `lucasac00/main`.

**Regras para PRs internos:**
- Título descritivo
- Descrição do que foi feito
- Referência à Issue relacionada (se houver)
- Verifique se os testes passam antes de abrir

---

## 3. Como enviar um PR limpo para o upstream (wagtail/wagtail)

O `main` do fork contém a pasta `videos/`, `docs-grupo/` e configurações de CI que **não devem** ir para o repositório original. Por isso, o PR para upstream deve sair de uma **branch limpa**:

```bash
# 1. Atualize a referência do upstream
git fetch upstream

# 2. Crie uma branch limpa a partir do upstream/main
git checkout -b pr-upstream upstream/main

# 3. Cherry-pick APENAS os commits de código relevantes (não inclua commits de videos/, docs-grupo/, CI interno)
git cherry-pick <hash-do-commit-1>
git cherry-pick <hash-do-commit-2>

# 4. Envie e abra o PR
git push -u origin pr-upstream
# No GitHub: pr-upstream → wagtail/wagtail:main
```

---

## 4. Comandos úteis

```bash
# Testes Python (Django)
python runtests.py
DATABASE_NAME=default.sqlite3 python runtests.py --parallel --keepdb --exclude-tag=transaction

# Testes JavaScript
npm run test:unit

# Cobertura
make coverage

# Lint
make lint

# Formatação
make format
```
