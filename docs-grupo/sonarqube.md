Para configurar o SonarCloud, fizemos o seguinte:

Criamos uma organização no sonarcloud.io: https://sonarcloud.io/organizations/es2-grupo03-ufscar/projects

Adicionamos o projeto lucasac00/wagtail

Configuramos "Github Actions" como método de análise, e adicionamos o SONAR_TOKEN aos secrets do repositório.

Depois, adicionamos a etapa do SonarCloud Scan ao workflow [ci-grupo.yml](/.github/workflows/ci-grupo.yml) e adicionamos o arquivo [sonar-project.properties](/sonar-project.properties) ao projeto.

No primeiro commit que adicionamos o SonarQube, ele já encontrou uma nova issue no próprio commit:\
Use full commit SHA hash for this dependency.
External GitHub Actions and workflows should be pinned to a commit hash githubactions:S7637

Essa issue estava na seguinte linha do ci-grupo.yml:\
`uses: sonarsource/sonarcloud-github-action@v2`

O problema é o uso direto da tag v2. O SonarQube aponta isso como uma issue de segurança de severidade alta pois podem acontecer ataques de supply chain, por isso é mais seguro fixar a versão usando o código do commit específico, que pode ser encontrado usando:\
`git ls-remote https://github.com/sonarsource/sonarcloud-github-action.git refs/tags/v2`

Agora, a linha fica:\
`uses: sonarsource/sonarcloud-github-action@e44258b109568baa0df60ed515909fc6c72cba92`
