Para configurar o SonarCloud, fizemos o seguinte:

Criamos uma organização no sonarcloud.io: https://sonarcloud.io/organizations/es2-grupo03-ufscar/projects

Adicionamos o projeto lucasac00/wagtail

Configuramos "Github Actions" como método de análise, e adicionamos o SONAR_TOKEN aos secrets do repositório.

Depois, adicionamos a etapa do SonarCloud Scan ao workflow [ci-grupo.yml](/.github/workflows/ci-grupo.yml) e adicionamos o arquivo [sonar-project.properties](/sonar-project.properties) ao projeto.

