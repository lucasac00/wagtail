# Correção de Warning SonarCloud — Lucas Cardoso

## Warning original

**Regra:** `pythonenterprise:S8437` — Class-Based Views should override `get_context_data` correctly

**Severidade:** High (Reliability)

**Arquivo:** `wagtail/admin/views/pages/delete.py`, linha 89

**Mensagem:** Call `super().get_context_data(**kwargs)` in this method.

## Causa

O método `get_context_data` da classe `DeleteView` sobrescrevia o método da classe pai (`TemplateView`) sem invocar `super()`. Isso descartava o contexto padrão injetado pelo Django (como `view`, parâmetros de URL, etc.).

### Código original

```python
def get_context_data(self, **kwargs):
    descendant_count = self.page.get_descendant_count()
    return {
        "page": self.page,
        "descendant_count": descendant_count,
        "next": self.next_url,
        # ... demais chaves de contexto
    }
```

O dicionário era criado do zero, sem mesclar com o contexto da classe base.

## Correção

Chamar `super().get_context_data(**kwargs)` e então complementar o dicionário com `update()`:

### Código corrigido

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    descendant_count = self.page.get_descendant_count()
    context.update(
        {
            "page": self.page,
            "descendant_count": descendant_count,
            "next": self.next_url,
            # ... demais chaves de contexto
        }
    )
    return context
```

## Verificação

Os 14 testes existentes da view de deleção continuam passando (`wagtail.admin.tests.pages.test_delete_page`). A correção não altera o comportamento visível, apenas garante conformidade com o padrão de Class-Based Views do Django.
