# ==========================================================
# ARQUIVO: github_api.py
# RESPONSABILIDADE: Conectar à API do GitHub e buscar dados.
# ==========================================================

import urllib.request
import urllib.error
import json
from functools import lru_cache

# --- Erros Personalizados ---
# Definir nossos próprios erros torna o app principal mais limpo
# Ele não precisará saber sobre 'urllib.error'.
class ApiError(Exception):
    """Erro genérico de comunicação com a API"""
    pass

class UserNotFoundError(ApiError):
    """Erro específico para quando o usuário não é encontrado (404)"""
    pass

# --- Função de Chamada Interna ---
@lru_cache(maxsize=128)
def _make_api_call(url):
    """
    Função auxiliar "privada" que faz a chamada de rede,
    trata erros e retorna os dados em Python.
    """
    try:
        # A API do GitHub exige um User-Agent na requisição
        headers = {'User-Agent': 'Python-GitHub-Activity-App'}
        # Cria um objeto de requisição, onde pode anexar info extras como os headers
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                #  Lê os bytes
                data_bytes = response.read()
                #  Decodifica para string
                data_string = data_bytes.decode('utf-8')
                #  Traduz de JSON para Python
                return json.loads(data_string)
            else:
                raise ApiError(f"API retornou status inesperado: {response.status}")
                
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # Lança erro personalizado
            raise UserNotFoundError(f"URL não encontrada: {url}")
        else:
            raise ApiError(f"Erro HTTP: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        raise ApiError(f"Erro de conexão. Verifique sua internet. Detalhes: {e.reason}")
    except json.JSONDecodeError:
        raise ApiError("Erro: Falha ao traduzir a resposta JSON da API.")

# --- Funções Públicas  ---

def get_user_events(username):
    """
    Busca a lista de eventos de um usuário.
    """
    print(f"Buscando eventos para {username}...")
    url = f"https://api.github.com/users/{username}/events"
    # Chama a função interna
    return _make_api_call(url)

def get_commit_count(repo_name, sha_before, sha_head):
    """
    Busca a contagem de commits entre dois SHAs.
    """
    url = f"https://api.github.com/repos/{repo_name}/compare/{sha_before}...{sha_head}"
    try:
        compare_data = _make_api_call(url)
        # .get() para evitar KeyErrors se a chave 'commits' não existir, retorna lista vazia
        commits_list = compare_data.get('commits', [])
        return len(commits_list)
    except ApiError as e:
        # Se a chamada de comparação falhar, não quebr o app,
        # apenas avisa no console e retorna None.
        print(f" (Aviso: não foi possível buscar contagem de commits: {e})")
        return None