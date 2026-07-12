# Compilando, executando e testando o Wagtail localmente

## Pré-requisitos

- Python >= 3.10
- [Node.js](https://nodejs.org/) (versão correspondente ao `.nvmrc` — use [fnm](https://github.com/Schniz/fnm) para alinhamento automático)
- Bibliotecas de sistema para o Pillow: **libjpeg** e **zlib**

---

## Passo a passo: do clone inicial a um site Wagtail funcionando

### 1. Clone o repositório

```
git clone https://github.com/wagtail/wagtail.git
cd wagtail
```

### 2. Crie e ative um virtualenv Python

```
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências de sistema (Ubuntu/Debian)

```
sudo apt-get install libjpeg-dev zlib1g-dev
```

### 4. Instale a versão correta do Node.js

Com fnm:
```
fnm install
```

Como alternativa, instale manualmente a versão exata declarada no `.nvmrc`.

### 5. Instale o Wagtail em modo de desenvolvimento/edição

```
pip install -e ".[testing,docs]"
```

### 6. Instale as dependências JS e compile os assets do frontend

```
npm ci
npm run build
```

> **Dica:** use `npm start` em vez de `npm run build` para observar alterações e recompilar automaticamente durante o desenvolvimento.

### 7. Configure o projeto de teste integrado

O Wagtail inclui um projeto Django de teste completo em `wagtail/test/`. Configure o banco de dados (SQLite com armazenamento persistente):

```
DATABASE_NAME=wagtail_local.db DJANGO_SETTINGS_MODULE=wagtail.test.settings python wagtail/test/manage.py migrate
```

### 8. Crie a tabela de cache (necessária para o projeto de teste)

```
DATABASE_NAME=wagtail_local.db DJANGO_SETTINGS_MODULE=wagtail.test.settings python wagtail/test/manage.py createcachetable
```

### 9. Crie um superusuário

```
DATABASE_NAME=wagtail_local.db DJANGO_SETTINGS_MODULE=wagtail.test.settings python wagtail/test/manage.py createsuperuser
```

Siga as instruções para definir nome de usuário, email e senha.

### 10. Inicie o servidor de desenvolvimento

```
DATABASE_NAME=wagtail_local.db DJANGO_SETTINGS_MODULE=wagtail.test.settings python wagtail/test/manage.py runserver
```

> A variável de ambiente `DATABASE_NAME` garante que o banco SQLite seja gravado em um arquivo (`wagtail_local.db`) em vez de ficar em memória, para que seus dados persistam entre reinicializações.

### 11. Abra no navegador

Acesse **http://127.0.0.1:8000/admin/** e faça login com as credenciais de superusuário que você acabou de criar.

O projeto de teste inclui o admin do Wagtail, imagens, documentos, busca, snippets e um `testapp` com vários modelos de página para experimentar.

---

## Executando os testes Python (módulo wagtail)

- **Todos os testes (SQLite, sem Elasticsearch)**:

  ```
  python runtests.py
  ```

- **Execução mais rápida** (paralela + manter BD):

  ```
  DATABASE_NAME=default.sqlite3 python runtests.py --parallel --keepdb --exclude-tag=transaction
  ```

- **Apenas um módulo/teste específico**:

  ```
  python runtests.py wagtail.admin
  python runtests.py -- wagtail.tests.test_blocks.TestIntegerBlock
  ```

- **Com PostgreSQL**: `python runtests.py --postgres`
- **Com Elasticsearch**: `python runtests.py --elasticsearch8`
- **Com tox** (múltiplas combinações Python/Django): `tox -l` para listar ambientes, depois, por exemplo, `tox -e py312-dj52-sqlite-noelasticsearch`

## Referência rápida do Makefile

| Comando | O que faz |
|---------|-----------|
| `make develop` | pip install + npm install + npm run build |
| `make test` | Executa os testes Python via `runtests.py` |
| `make lint` | Executa toda a verificação de lint (Python, JS, CSS, docs) |
| `make format` | Formata automaticamente todo o código |
| `make coverage` | Relatório de cobertura de testes |

E para testes JS do frontend: `npm run test:unit` (testes unitários com Jest).
