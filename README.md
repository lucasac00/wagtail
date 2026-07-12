# Engenharia de Software 2 - Grupo 03
Arthur Fonseca -  811461\
Julia Tavares dos Santos - 820872\
Lucas Cardoso - 813583\
Luisa Tavares dos Santos - 820990\
Samuel Said - 800209

[Link para o README original](/README_og.md)

Estrutura de pastas:\
[videos](/videos): Contém os vídeos criados durante o desenvolvimento do projeto\
[docs-grupo](/docs-grupo): Contém os documentos criados durante o desenvolvimento do projeto

O restante do repositório é idêntico ao [Wagtail original](https://github.com/wagtail/wagtail), com adição apenas das pastas `videos/` e `docs-grupo/`.

## Remotes
Este repositório é um fork. Trabalhamos com dois remotes:

| Remote | URL | Finalidade |
|-|-|-|
| `origin` | `git@github.com:lucasac00/wagtail.git` | Fork do grupo — onde commits, branches e PRs internos são feitos |
| `upstream` | `git@github.com:wagtail/wagtail.git` | Repositório original — usado para sincronizar atualizações e como base para o PR final |

O `main` do fork contém commits exclusivos do grupo (`videos/`, `docs-grupo/`). O PR para o upstream sairá de uma branch limpa baseada em `upstream/main`, contendo apenas os commits de código relevantes (via cherry-pick). Veja o [guia de contribuição](docs-grupo/guia-contribuicao.md).

