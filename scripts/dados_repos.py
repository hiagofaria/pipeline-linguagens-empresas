import requests
import pandas as pd

class DadosRepositorios:
    """
    Responsável por extrair informações dos repositórios
    de uma conta do GitHub por meio da API.
    """

    def __init__(self, owner):
        """
        Inicializa a classe com os dados necessários para
        acessar os repositórios de uma conta do GitHub.

        Args:
            owner (str): Nome da conta do GitHub.
            access_token (str): Token utilizado na autenticação.
        """
        self.owner = owner
        self.api_base_url = 'https://api.github.com'
        self.access_token='COLOQUE_SEU_TOKEN'
        self.headers = {'Authorization': 'Bearer ' + self.access_token,
                    'X-GitHub-Api-Version': '2022-11-28'}


    def lista_repositorios (self):
        """
        Extrai os repositórios da conta informada, percorrendo
        as páginas disponibilizadas pela API do GitHub.

        Returns:
            list: Lista contendo os dados dos repositórios extraídos.
        """
        repos_list = []

        for page_num in range(1, 20):
            try:
                url = f'{self.api_base_url}/users/{self.owner}/repos?page={page_num}'
                response = requests.get(url, headers=self.headers)
                repos_list.append(response.json())
            except:
                repos_list.append(None)
                
        return repos_list