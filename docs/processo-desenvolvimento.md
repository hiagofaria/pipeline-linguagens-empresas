# Processo de Desenvolvimento

Este documento apresenta as etapas de desenvolvimento do projeto, desde a exploração inicial da API REST do GitHub no Jupyter Notebook até a construção de scripts Python reutilizáveis para extração e armazenamento de dados de diferentes organizações.

## 1. Exploração da API REST do GitHub

O desenvolvimento começou com o estudo da API REST do GitHub, utilizando a biblioteca Requests para realizar requisições HTTP e consultar informações dos repositórios.

Inicialmente, foram explorados os seguintes conceitos:

- Requisições HTTP utilizando o método GET.
- Endpoints da API do GitHub.
- Códigos de status das respostas HTTP.
- Visualização e conversão de respostas JSON em objetos Python.
- Definição de cabeçalhos HTTP e versão da API.

Essa etapa permitiu compreender como realizar consultas à API e acessar as informações disponibilizadas pelos repositórios.

## 2. Extração dos dados da Amazon

Após compreender o funcionamento das requisições, foi iniciada a extração dos dados dos repositórios da Amazon, identificada pelo usuário `amzn` no GitHub.

A consulta inicial retornou apenas 30 dos 132 repositórios disponíveis, o que levou à investigação dos limites de requisições da API e da necessidade de implementar autenticação e paginação.

### 2.1 Autenticação

Para ampliar o limite de requisições à API, foi utilizada a autenticação por meio de um Personal Access Token (PAT) do GitHub.

O token foi inserido no cabeçalho HTTP `Authorization`, permitindo realizar as consultas de forma autenticada.

Também foi definido o cabeçalho `X-GitHub-Api-Version` para especificar a versão da API utilizada.

### 2.2 Paginação

Como a API retorna os resultados divididos em páginas, foi implementado um laço de repetição para percorrer diferentes páginas e reunir os repositórios consultados em uma única lista.

Essa abordagem permitiu ampliar a quantidade de dados coletados em relação à requisição inicial.

No notebook, a exploração utilizou cinco páginas de consulta.

## 3. Transformação e organização dos dados

Com os dados retornados pela API, foi necessário extrair as informações relevantes para o projeto.

Foram criadas listas para armazenar:

- Os nomes dos repositórios.
- As linguagens de programação principais identificadas pela API.

Em seguida, foi utilizada a biblioteca Pandas para organizar essas informações em um DataFrame com duas colunas:

| Coluna | Descrição |
|---|---|
| `repository_name` | Nome do repositório no GitHub. |
| `language` | Linguagem de programação principal identificada pela API. |

Após a organização, o DataFrame foi exportado para um arquivo CSV utilizando o método `to_csv()`, armazenando os dados extraídos da Amazon.

## 4. Armazenamento dos dados no GitHub

Após a exportação do CSV, foi explorada a possibilidade de armazenar o resultado diretamente em um repositório do GitHub, utilizando novamente sua API REST.

Essa etapa envolveu duas operações principais.

### 4.1 Criação do repositório

Foi utilizada uma requisição HTTP POST para criar um repositório público na conta autenticada do GitHub.

O corpo da requisição foi enviado em formato JSON, contendo o nome, a descrição e a configuração de visibilidade do repositório.

O repositório criado nessa etapa foi:

[linguagens-utilizadas](https://github.com/hiagofaria/linguagens-utilizadas)

Ele contém o arquivo `amazon.csv`, resultado da exploração inicial realizada no notebook.

### 4.2 Codificação e envio do arquivo

Para realizar o upload do CSV por meio da API, foi utilizada a biblioteca Base64.

O processo consistiu em:

1. Abrir o arquivo CSV em modo binário (`rb`).
2. Ler seu conteúdo utilizando `read()`.
3. Codificar os dados com `base64.b64encode()`.
4. Converter o conteúdo codificado para uma string utilizando `decode('utf-8')`.
5. Enviar o arquivo por meio de uma requisição HTTP PUT.

A requisição foi direcionada ao endpoint de conteúdos do repositório, contendo o nome do arquivo e seu conteúdo codificado em Base64.

Com isso, foi possível concluir a primeira implementação: extrair os dados da Amazon, organizá-los em um DataFrame, exportá-los para CSV e enviá-los ao GitHub.

## 5. Generalização do processo com Python

Após concluir a exploração no Jupyter Notebook, o processo foi transformado em scripts Python, com o objetivo de reutilizar a lógica desenvolvida e permitir a extração de dados de diferentes contas ou organizações do GitHub.

Essa mudança também permitiu separar as responsabilidades do código em duas classes.

### 5.1 Classe DadosRepositorios

A classe `DadosRepositorios` ficou responsável pela extração e organização das informações dos repositórios.

Seu construtor recebe dois parâmetros:

- `owner`: nome de usuário ou organização que será consultada.
- `access_token`: token utilizado para autenticação na API.

A classe possui os seguintes métodos:

| Método | Responsabilidade |
|---|---|
| `lista_repositorios()` | Realiza as requisições à API e reúne os resultados das páginas consultadas. |
| `nomes_repos()` | Extrai os nomes dos repositórios. |
| `nomes_linguagens()` | Extrai as linguagens principais dos repositórios. |
| `cria_df_linguagens()` | Organiza os nomes e as linguagens em um DataFrame. |

A paginação foi incorporada à classe, permitindo consultar até 19 páginas por execução, conforme definido no código.

Com essa estrutura, a mesma lógica passou a ser utilizada para diferentes organizações, sem precisar desenvolver um processo de extração separado para cada uma.

### 5.2 Extração de diferentes organizações

A classe foi instanciada para três organizações:

- Amazon (`amzn`).
- Netflix (`netflix`).
- Spotify (`spotify`).

Cada instância realiza a consulta correspondente e gera um DataFrame com os nomes dos repositórios e suas respectivas linguagens principais.

Dessa forma, o processo inicialmente desenvolvido para a Amazon passou a ser reutilizável para diferentes contas do GitHub.

### 5.3 Exportação dos arquivos CSV

Após a criação dos DataFrames, os resultados foram exportados separadamente para a pasta `data_processed/`, utilizando o método `to_csv()` do Pandas.

Foram gerados os seguintes arquivos:

- `linguagens_amzn.csv`
- `linguagens_netflix.csv`
- `linguagens_spotify.csv`

Cada arquivo mantém a mesma estrutura de colunas, facilitando a organização e o consumo dos dados.

## 6. Generalização do envio dos arquivos ao GitHub

Assim como a extração, a etapa de armazenamento também foi reorganizada em uma classe Python.

### 6.1 Classe ManipulaRepositorios

A classe `ManipulaRepositorios` ficou responsável por realizar a criação de repositórios e o envio dos arquivos CSV por meio da API REST do GitHub.

Seu construtor recebe o nome de usuário da conta GitHub e configura o token de autenticação e os cabeçalhos utilizados nas requisições.

A classe possui dois métodos principais:

| Método | Responsabilidade |
|---|---|
| `cria_repo()` | Envia uma requisição POST para criar um repositório público. |
| `add_arquivo()` | Lê um arquivo local, codifica seu conteúdo em Base64 e envia ao repositório por meio de uma requisição PUT. |

### 6.2 Envio dos três arquivos

Na versão generalizada, foi definido um novo repositório de destino:

[linguagens-repositorios-empresas](https://github.com/hiagofaria/linguagens-repositorios-empresas)

Diferentemente do repositório criado durante a exploração inicial, esse repositório reúne os resultados das três organizações consultadas.

Os arquivos gerados na etapa de extração são enviados individualmente, utilizando o método `add_arquivo()`.

Assim, a etapa de armazenamento também passou a ser reutilizável, evitando a necessidade de implementar manualmente uma requisição de upload para cada arquivo.

## 7. Resultado do desenvolvimento

O projeto evoluiu de uma exploração inicial da API do GitHub, focada exclusivamente nos repositórios da Amazon, para uma implementação estruturada em classes Python.

Essa evolução permitiu:

- Reutilizar a lógica de extração para diferentes organizações.
- Organizar as responsabilidades de extração e armazenamento em classes distintas.
- Utilizar Pandas para estruturar e exportar os dados.
- Automatizar a criação de repositórios e o envio de arquivos por meio da API do GitHub.
- Separar os resultados da exploração inicial daqueles produzidos pela versão generalizada.

O resultado é um processo reutilizável para consultar informações de repositórios do GitHub, organizar suas linguagens principais e armazenar os resultados em arquivos CSV.

## 8. Organização dos repositórios de destino

O projeto possui dois repositórios de destino, cada um relacionado a uma etapa diferente do desenvolvimento:

| Repositório | Finalidade |
|---|---|
| [linguagens-utilizadas](https://github.com/hiagofaria/linguagens-utilizadas) | Armazenar o resultado da exploração inicial realizada no Jupyter Notebook, contendo os dados da Amazon. |
| [linguagens-repositorios-empresas](https://github.com/hiagofaria/linguagens-repositorios-empresas) | Armazenar os arquivos CSV gerados pela versão generalizada dos scripts, contendo dados da Amazon, Netflix e Spotify. |

Essa separação mantém o histórico da evolução do projeto e diferencia a primeira implementação da versão reutilizável.