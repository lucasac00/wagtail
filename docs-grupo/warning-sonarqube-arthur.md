# Correção de Warning SonarCloud — Arthur Fonseca

## Warning original

**Regra:** `python:S930` — Function calls should not pass extra arguments (nem omitir argumentos obrigatórios)

**Severidade:** Blocker (Reliability)

**Arquivo:** `wagtail/contrib/frontend_cache/backends/dummy.py`, linha 6

**Mensagem:** Add 1 missing arguments; '__init__' expects 1 positional arguments.

## Causa

O construtor de `DummyBackend` não aceitava argumentos e chamava `super().__init__()` sem repassar nada. Porém, a classe pai `BaseBackend` exige o parâmetro `params` no construtor:

```python
# wagtail/contrib/frontend_cache/backends/base.py
class BaseBackend:
    def __init__(self, params):
        self.hostnames = params.get("HOSTNAMES", ["*"])
```

E o caminho real de instanciação dos backends de cache, em `wagtail/contrib/frontend_cache/utils.py` (função `get_backends`), sempre passa a configuração como argumento posicional:

```python
backend_objects[backend_name] = backend_cls(backend_config)
```

Ou seja, qualquer tentativa de configurar o `DummyBackend` via `WAGTAILFRONTENDCACHE` quebrava imediatamente com:

```
TypeError: DummyBackend.__init__() takes 1 positional argument but 2 were given
```

O bug nunca havia sido percebido porque nada no repositório instanciava a classe pelo caminho normal — mas ela existe justamente para ser usada como backend "fake" em desenvolvimento/testes, e estava inutilizável.

### Código original

```python
class DummyBackend(BaseBackend):
    def __init__(self):
        super().__init__()

        self.urls = []
```

## Correção

Aceitar `params` na assinatura e repassá-lo ao construtor da classe pai, como todos os demais backends fazem:

### Código corrigido

```python
class DummyBackend(BaseBackend):
    def __init__(self, params):
        super().__init__(params)

        self.urls = []
```

Como `BaseBackend` usa `params.get("HOSTNAMES", ["*"])`, nenhuma chave é obrigatória — um dicionário de configuração vazio continua funcionando.

## Verificação

Foi adicionado o teste de regressão `test_dummy` em `wagtail/contrib/frontend_cache/tests.py` (classe `TestBackendConfiguration`), que configura o `DummyBackend` via `get_backends()` — o mesmo caminho de produção:

- **Antes da correção**, o teste falha com `TypeError: DummyBackend.__init__() takes 1 positional argument but 2 were given`, reproduzindo o problema apontado pelo SonarCloud.
- **Depois da correção**, o teste passa, e os 44 testes do módulo `wagtail.contrib.frontend_cache` continuam passando (`python runtests.py wagtail.contrib.frontend_cache`).
