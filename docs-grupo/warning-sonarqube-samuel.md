# Correção de Warning SonarCloud — Samuel Said

## Warning original

**Regra:** `python:S3699` — The output of functions that don't return anything should not be used

**Severidade:** Major — Bug (Reliability: Medium)

**Arquivo:** `wagtail/admin/panels/group.py`, linha 62

**Mensagem:** Remove this use of the output from "extend"; "extend" doesn’t return anything.

## Causa

No método `PanelGroup.get_form_options`, ao mesclar as opções de formulário vindas dos painéis-filhos, o ramo que trata um valor do tipo `tuple` fazia:

```python
options[key] = list(current_val).extend(new_val)
```

O método `list.extend()` altera a lista **no lugar** e retorna `None`. Como o retorno estava sendo atribuído a `options[key]`, essa chave recebia `None` em vez da lista mesclada — descartando silenciosamente os valores combinados de `current_val` e `new_val`.

### Código original

```python
elif isinstance(current_val, tuple) and isinstance(
    new_val, (list, tuple)
):
    options[key] = list(current_val).extend(new_val)
```

## Correção

Criar a lista a partir de `current_val`, estendê-la com `new_val` numa instrução separada e só então atribuí-la a `options[key]`. Assim a chave recebe a lista mesclada, e não `None`.

### Código corrigido

```python
elif isinstance(current_val, tuple) and isinstance(
    new_val, (list, tuple)
):
    merged = list(current_val)
    merged.extend(new_val)
    options[key] = merged
```

## Verificação

A correção não altera a interface do método, apenas garante o resultado correto no ramo de mesclagem de tuplas. Os testes existentes dos painéis continuam passando (`wagtail.admin.tests.test_edit_handlers`), e o comportamento passa a ser o pretendido: `options[key]` recebe a lista com os itens de `current_val` seguidos dos de `new_val`, em vez de `None`. Não há redução de cobertura nem regressão na suíte.
