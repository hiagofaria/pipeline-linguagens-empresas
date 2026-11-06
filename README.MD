# Pipeline de Linguagens de Programação — Empresas

Projeto desenvolvido em Python que utiliza a API REST do GitHub para extrair informações dos repositórios de diferentes organizações, identificar suas linguagens de programação principais e armazenar os resultados em arquivos CSV.

## Tecnologias utilizadas

- **Python:** desenvolvimento dos scripts de extração e manipulação dos dados.
- **Requests:** realização de requisições HTTP à API do GitHub.
- **Pandas:** organização dos dados em DataFrames e exportação para CSV.
- **Jupyter Notebook:** exploração inicial da API e desenvolvimento da primeira implementação.
- **GitHub REST API:** consulta de repositórios, criação de repositórios e envio de arquivos.
- **Base64:** codificação do conteúdo dos arquivos para envio por meio da API do GitHub.

## Estrutura do projeto

```text
pipeline-linguagens-empresas/
│
├── data_processed/
│   ├── linguagens_amzn.csv
│   ├── linguagens_netflix.csv
│   └── linguagens_spotify.csv
│
├── notebook/
│   └── linguagens_repos.ipynb
│
├── scripts/
│   ├── dados_repos.py
│   └── manipula_repos.py
│
└── .gitignore
```

## Resultados

O projeto contempla a extração de informações de três organizações:

| Organização | Registros |
|---|---:|
| Amazon | 178 |
| Netflix | 239 |
| Spotify | 289 |
| **Total** | **706** |

Os arquivos CSV possuem duas colunas:

- `repository_name`: nome do repositório.
- `language`: linguagem de programação principal identificada pela API do GitHub.

Alguns registros apresentam valores nulos na coluna `language`, quando a API não identifica uma linguagem principal para determinado repositório.

## Repositórios de dados

Os resultados estão armazenados em dois repositórios distintos, correspondentes às etapas do projeto:

- [linguagens-utilizadas](https://github.com/hiagofaria/linguagens-utilizadas): contém os dados da Amazon, gerados durante a exploração inicial no Jupyter Notebook.
- [linguagens-repositorios-empresas](https://github.com/hiagofaria/linguagens-repositorios-empresas): contém os dados da Amazon, Netflix e Spotify, gerados pela versão generalizada dos scripts Python.

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/hiagofaria/pipeline-linguagens-empresas.git
cd pipeline-linguagens-empresas
```

### 2. Criar e ativar um ambiente virtual

**Linux/WSL:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install requests pandas
```

### 4. Configurar o token do GitHub

Para executar os scripts, é necessário possuir um Personal Access Token do GitHub.

Nos arquivos `scripts/dados_repos.py` e `scripts/manipula_repos.py`, substitua o marcador `COLOQUE_SEU_TOKEN` pelo seu próprio token.

O token deve possuir as permissões necessárias para consultar os repositórios, criar um repositório público e enviar arquivos.

### 5. Configurar o usuário do GitHub

No arquivo `scripts/manipula_repos.py`, informe seu próprio nome de usuário do GitHub na instanciação da classe `ManipulaRepositorios`.

### 6. Executar a extração dos dados

Na raiz do projeto, execute:

```bash
python scripts/dados_repos.py
```

Os dados serão extraídos das organizações configuradas no script e exportados para arquivos CSV na pasta `data_processed/`.

### 7. Criar o repositório e enviar os arquivos

Após a extração, execute:

```bash
python scripts/manipula_repos.py
```

O script realiza a criação de um repositório público na conta informada e o envio dos arquivos CSV.

**Observação:** a implementação atual está preparada para criar um novo repositório. Caso o repositório já exista, a criação poderá retornar um erro. A atualização de arquivos já existentes não está implementada.

## Segurança

- Utilize seu próprio Personal Access Token.
- Não compartilhe suas credenciais.
- Não publique tokens reais no GitHub.
- Substitua o marcador `COLOQUE_SEU_TOKEN` apenas localmente, antes da execução dos scripts.

## Documentação

Para conhecer as etapas de construção, decisões técnicas e evolução do projeto, consulte o documento [Processo de Desenvolvimento](docs/processo-desenvolvimento.md).