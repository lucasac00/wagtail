O Wagtail [já tem workflows no Github Actions](/.github/workflows/test.yml).
Decidimos criar um workflow próprio do grupo, que seja simples e funcional. Não vamos usar todos os workflows pesados já existentes.

O workflow fará:
1. Python tests com SQLite (`python runtests.py`)
2. Coverage Report (`make coverage`)
3. JS unit tests (`npm run test:unit`)

[ci-grupo.yml](/.github/workflows/ci-grupo.yml)



