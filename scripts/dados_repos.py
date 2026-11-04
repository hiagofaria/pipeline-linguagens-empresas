
import os
import requests
import pandas as pd


class DadosRepositorios:
    """
    Realiza a extração e organização de informações dos repositórios
    de uma conta do GitHub por meio da API REST.
    """

    def __init__(self, owner, access_token):
        """
        Inicializa a classe com as informações necessárias para
        acessar os repositórios de uma conta do GitHub.

        Args:
            owner (str): Nome de usuário ou organização no GitHub.
            access_token (str): Token utilizado para autenticação
                nas requisições à API.
        """
        self.owner = owner
        self.api_base_url = 'https://api.github.com'
        self.access_token = access_token

        # Define os cabeçalhos utilizados na comunicação com a API.
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-GitHub-Api-Version': '2022-11-28'
        }

    def lista_repositorios(self):
        """
        Consulta os repositórios da conta informada na API do GitHub,
        percorrendo as páginas disponíveis.

        Returns:
            list: Lista contendo as respostas da API para cada página
            consultada.
        """
        repos_list = []

        # Percorre as páginas da API para obter os repositórios.
        for page_num in range(1, 20):
            try:
                url = f'{self.api_base_url}/users/{self.owner}/repos?page={page_num}'
                response = requests.get(url, headers=self.headers)
                repos_list.append(response.json())
            except:
                repos_list.append(None)

        return repos_list

    def nomes_repos(self, repos_list):
        """
        Extrai os nomes dos repositórios presentes nas páginas
        recebidas da API do GitHub.

        Args:
            repos_list (list): Lista contendo os dados dos repositórios.

        Returns:
            list: Lista com os nomes dos repositórios encontrados.
        """
        repo_names = []

        # Percorre as páginas e extrai o nome de cada repositório.
        for page in repos_list:
            for repo in page:
                try:
                    repo_names.append(repo['name'])
                except:
                    pass

        return repo_names

    def nomes_linguagens(self, repos_list):
        """
        Extrai as linguagens principais utilizadas nos repositórios
        presentes nas páginas recebidas da API.

        Args:
            repos_list (list): Lista contendo as linguagens principais
                dos repositórios.

        Returns:
            list: Lista com as linguagens principais dos repositórios.
        """
        repo_languages = []

        # Percorre as páginas e extrai a linguagem de cada repositório.
        for page in repos_list:
            for repo in page:
                try:
                    repo_languages.append(repo['language'])
                except:
                    pass

        return repo_languages

    def cria_df_linguagens(self):
        """
        Organiza os nomes dos repositórios e suas respectivas
        linguagens principais em um DataFrame.

        Returns:
            pandas.DataFrame: DataFrame com as colunas
            repository_name e language.
        """
        # Obtém os dados dos repositórios por meio da API.
        repositorios = self.lista_repositorios()

        # Extrai os nomes e as linguagens dos repositórios.
        nomes = self.nomes_repos(repositorios)
        linguagens = self.nomes_linguagens(repositorios)

        # Organiza as informações em um DataFrame.
        dados = pd.DataFrame()
        dados['repository_name'] = nomes
        dados['language'] = linguagens

        return dados


# Execução do processo

# Insira seu próprio token de acesso do GitHub.
access_token = 'COLOQUE_SEU_TOKEN'

print('Token disponível:', bool(access_token))

# Interrompe a execução caso o token não tenha sido substituído.
if access_token == 'COLOQUE_SEU_TOKEN':
    raise ValueError('Insira seu próprio token de acesso do GitHub.')

print('\nIniciando extração dos repositórios...')


# Extração dos repositórios da Amazon.
amazon_rep = DadosRepositorios('amzn', access_token)
ling_mais_usadas_amzn = amazon_rep.cria_df_linguagens()

print('\nExtração da Amazon finalizada!')
print(ling_mais_usadas_amzn)
print('Quantidade de repositórios:', len(ling_mais_usadas_amzn))


# Extração dos repositórios da Netflix.
netflix_rep = DadosRepositorios('netflix', access_token)
ling_mais_usadas_netflix = netflix_rep.cria_df_linguagens()

print('\nExtração da Netflix finalizada!')
print(ling_mais_usadas_netflix)
print('Quantidade de repositórios:', len(ling_mais_usadas_netflix))


# Extração dos repositórios do Spotify.
spotify_rep = DadosRepositorios('spotify', access_token)
ling_mais_usadas_spotify = spotify_rep.cria_df_linguagens()

print('\nExtração do Spotify finalizada!')
print(ling_mais_usadas_spotify)
print('Quantidade de repositórios:', len(ling_mais_usadas_spotify))


# Armazenamento dos DataFrames em arquivos CSV.

ling_mais_usadas_amzn.to_csv('data_processed/linguagens_amzn.csv', index=False)
ling_mais_usadas_netflix.to_csv('data_processed/linguagens_netflix.csv', index=False)
ling_mais_usadas_spotify.to_csv('data_processed/linguagens_spotify.csv', index=False)

print('\nArquivos CSV salvos com sucesso!')
