# Correção da Issue #14388 — Samuel Said

## Issue original

**Origem:** [wagtail/wagtail#14388](https://github.com/wagtail/wagtail/issues/14388) — issue tracker do projeto original

**Tipo:** Bug (Reliability) — resposta HTTP 500 em vez de 404

**Arquivo:** `wagtail/admin/views/pages/bulk_actions/page_bulk_action.py`, linha 25

**Sintoma:** Numa ação em massa com "Select all in listing", a URL passa a conter `id=all&childOf=<page_id>`. Se a página referenciada por `childOf` não existir mais (por exemplo, apagada por outro admin enquanto a listagem estava aberta), a view estoura `Page.DoesNotExist` não tratado, resultando em erro 500.

## Causa

O método `get_all_objects_in_listing_query` chama `.get(id=parent_id)` diretamente. Quando `parent_id` aponta para uma página inexistente, o `QuerySet.get()` levanta `Page.DoesNotExist`, que não é tratado e vira um erro 500 em vez de uma resposta 404 adequada.

### Código original

```python
def get_all_objects_in_listing_query(self, parent_id):
    listing_objects = self.model.objects.all()

    q = None
    if "q" in self.request.GET:
        q = self.request.GET.get("q", "")

    if parent_id is not None:
        listing_objects = listing_objects.get(id=parent_id)
        # ... segue com get_descendants() / get_children()
```

## Correção

Substituir `.get(id=parent_id)` por `get_object_or_404(self.model, id=parent_id)` — abordagem idiomática do Django que devolve uma resposta 404 apropriada em vez de propagar a exceção (500). Foi a correção indicada pelo próprio autor da issue.

### Código corrigido

```python
from django.shortcuts import get_object_or_404

# ...

def get_all_objects_in_listing_query(self, parent_id):
    listing_objects = self.model.objects.all()

    q = None
    if "q" in self.request.GET:
        q = self.request.GET.get("q", "")

    if parent_id is not None:
        listing_objects = get_object_or_404(self.model, id=parent_id)
        # ... segue com get_descendants() / get_children()
```

## Verificação

Adicionado o teste de regressão `wagtail/admin/tests/pages/test_bulk_actions/test_bulk_action_childof.py`, com dois casos:

- `test_select_all_with_nonexistent_childof_returns_404` — garante 404 quando `childOf` aponta para página inexistente (antes retornava 500);
- `test_select_all_with_valid_childof_still_works` — garante que o caso válido continua respondendo 200 (sem regressão).

A correção não reduz cobertura (a linha nova é exercitada pelos testes) e não quebra a suíte existente. Esta é a contribuição selecionada para o pull request ao projeto original.
