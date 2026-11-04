
import requests
import base64


class ManipulaRepositorios:
    """
    Gerencia a criação de repositórios e o envio de arquivos
    por meio da API REST do GitHub.
    """

    def __init__(self, username):
        """
        Inicializa a classe com os dados de autenticação
        e acesso à API do GitHub.

        Args:
            username (str): Nome de usuário da conta GitHub.
        """
        self.username = username
        self.api_base_url = 'https://api.github.com'

        # Insira seu próprio token de acesso do GitHub.
        self.access_token = 'COLOQUE_SEU_TOKEN'

        # Define os cabeçalhos utilizados nas requisições à API.
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-GitHub-Api-Version': '2022-11-28'
        }

    def cria_repo(self, nome_repo):
        """
        Cria um repositório público na conta autenticada do GitHub.

        Args:
            nome_repo (str): Nome do repositório que será criado.
        """
        data = {
            "name": nome_repo,
            "description": "Dados dos repositórios de algumas empresas",
            "private": False
        }

        # Envia uma requisição POST para criar o repositório.
        response = requests.post(
            f"{self.api_base_url}/user/repos",
            json=data,
            headers=self.headers
        )

        print(f'status_code criação do repositório: {response.status_code}')

    def add_arquivo(self, nome_repo, nome_arquivo, caminho_arquivo):
        """
        Envia um arquivo local para um repositório no GitHub.

        Args:
            nome_repo (str): Nome do repositório de destino.
            nome_arquivo (str): Nome que o arquivo terá no GitHub.
            caminho_arquivo (str): Caminho local do arquivo que será enviado.
        """

        # Lê o conteúdo do arquivo em formato binário.
        with open(caminho_arquivo, "rb") as file:
            file_content = file.read()

        # Codifica o conteúdo do arquivo em Base64.
        encoded_content = base64.b64encode(file_content)

        # Define a URL do endpoint responsável pelo upload.
        url = (
            f"{self.api_base_url}/repos/{self.username}/"
            f"{nome_repo}/contents/{nome_arquivo}"
        )

        # Organiza os dados necessários para o envio do arquivo.
        data = {
            "message": "Adicionando um novo arquivo",
            "content": encoded_content.decode("utf-8")
        }

        # Envia uma requisição PUT para adicionar o arquivo ao repositório.
        response = requests.put(url, json=data, headers=self.headers)

        print(f'status_code upload do arquivo: {response.status_code}')


# Instanciando um objeto para manipular os repositórios.
novo_repo = ManipulaRepositorios('hiagofaria')

# Define o nome do repositório que será criado.
nome_repo = 'linguagens-repositorios-empresas'

# Cria o repositório no GitHub.
novo_repo.cria_repo(nome_repo)

# Envia os arquivos CSV gerados pelo processo de extração.
novo_repo.add_arquivo(
    nome_repo,
    'linguagens_amzn.csv',
    'data_processed/linguagens_amzn.csv'
)

novo_repo.add_arquivo(
    nome_repo,
    'linguagens_netflix.csv',
    'data_processed/linguagens_netflix.csv'
)

novo_repo.add_arquivo(
    nome_repo,
    'linguagens_spotify.csv',
    'data_processed/linguagens_spotify.csv'
)
