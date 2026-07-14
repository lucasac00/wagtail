# Correção da Issue #14382

## Issue original

**Origem:** [wagtail/wagtail#14382](https://github.com/wagtail/wagtail/issues/14382) — issue tracker do projeto original

**Tipo:** Bug, `__repr__` de `Vector` e `Rect` trunca coordenadas float

**Arquivo:** `wagtail/images/rect.py`, linhas 19 e 188

**Sintoma:** `Vector.__repr__` e `Rect.__repr__` usam formato `%d` (inteiro), truncando silenciosamente valores float para inteiros. Métodos como `_set_size()` e `_set_centroid()` usam divisão float e produzem coordenadas não-inteiras — o repr exibido não corresponde ao valor real.

## Causa

Os dois métodos `__repr__` formatavam as coordenadas com `%d`:

```python
# Vector
return "Vector(x: %d, y: %d)" % (self.x, self.y)

# Rect
return "Rect(left: %d, top: %d, right: %d, bottom: %d)" % (...)
```

`%d` converte qualquer valor para inteiro, descartando a parte decimal. Um `Vector(1.7, 3.9)` era exibido como `Vector(x: 1, y: 3)`, enganando durante debugging e logs.

## Correção

Substituir `%d` por f-strings com o especificador `:g`, que exibe floats sem trailing zeros desnecessários e preserva inteiros como inteiros:

### Código corrigido

```python
# Vector (linha 19)
def __repr__(self):
    return f"Vector(x: {self.x:g}, y: {self.y:g})"

# Rect (linha 188)
def __repr__(self):
    return (
        f"Rect(left: {self.left:g}, top: {self.top:g},"
        f" right: {self.right:g}, bottom: {self.bottom:g})"
    )
```

| Entrada | Antes | Depois |
|---------|-------|--------|
| `Vector(1.7, 3.9)` | `Vector(x: 1, y: 3)` | `Vector(x: 1.7, y: 3.9)` |
| `Vector(100, 150)` | `Vector(x: 100, y: 150)` | `Vector(x: 100, y: 150)` |
| `Rect(1.5, 1.5, 8.5, 8.5)` | `Rect(left: 1, top: 1, right: 8, bottom: 8)` | `Rect(left: 1.5, top: 1.5, right: 8.5, bottom: 8.5)` |

## Verificação

Os 637 testes da suíte de imagens (`wagtail.images.tests`) continuam passando. O teste `test_rect_repr` existente usa coordenadas inteiras e permanece inalterado — o formato `:g` mantém compatibilidade.
