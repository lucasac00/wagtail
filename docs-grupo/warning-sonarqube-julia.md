# Correção de Warning SonarCloud: Julia Tavares dos Santos

## Warning original

**Regra:** `python:S1481:` Unused local variables should be removed

**Severidade:** Minor (Maintainability)

**Arquivo:** `wagtail/admin/compare.py`, classe ChildRelationComparison

**Ocorrências:**
Linha 657, método get_child_comparisons — "Replace the unused local variable map_forwards with _."
Linha 685, método has_changed — "Replace the unused local variable map_backwards with _."

## Causa
O método `get_mapping` retorna uma tupla de 4 valores:
map_forwards, map_backwards, added e deleted. 
Em dois pontos diferentes do arquivo essa tupla era desempacotada por completo, mas em cada um dos dois métodos apenas 3 dos 4 valores eram utilizados

# Código original
## ChildRelationComparison.get_child_comparisons (linha 657)
map_forwards, map_backwards, added, deleted = self.get_mapping(objs_a, objs_b)
objs_a = dict(enumerate(objs_a))
objs_b = dict(enumerate(objs_b))

`map_forwards nunca é lido depois desta linha`

## ChildRelationComparison.has_changed (linha 685)
map_forwards, map_backwards, added, deleted = self.get_mapping(objs_a, objs_b)
if added or deleted:
    return True
for a_idx, b_idx in map_forwards.items():
    ...
    
`map_backwards nunca é lido depois desta linha`

## Correção
Substituí, em cada método, apenas a variável que não era utilizada pelo identificador _, uma convenção do Python para indicar que um valor está sendo descartado de forma intencional. Nenhum comportamento do código mudou.

# Código corrigido
## get_child_comparisons
_, map_backwards, added, deleted = self.get_mapping(objs_a, objs_b)

## has_changed
map_forwards, _, added, deleted = self.get_mapping(objs_a, objs_b)

Enviado no PR#11 (fix/sonar-unused-mapping-vars).