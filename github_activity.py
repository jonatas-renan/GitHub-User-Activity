# ==========================================================
# ARQUIVO: github_activity.py
# RESPONSABILIDADE: Interagir com o usuário (CLI) e formatar a saída.
# ==========================================================

import sys
import github_api

def format_event_string(event):
    """
    Recebe um único dicionário de evento (ações que o usuário realizou) e retorna a string formatada para impressão.
    """
    tipo_evento = event['type']
    
    if 'repo' in event and event['repo']:
        nome_repo = event['repo']['name']
    else:
        nome_repo = "[Repositório Privado ou Deletado]"

    # --- Lógica de Formatação ---
    if tipo_evento == 'PushEvent':
        # Pega os SHAs (identificadores únicos de commit)
        # 'before' é o SHA do commit antigo, 'head' é o SHA do commit novo
        sha_before = event['payload']['before']
        sha_head = event['payload']['head']
        
        # Chama o módulo de API para fazer a 2ª chamada
        commits_count = github_api.get_commit_count(nome_repo, sha_before, sha_head)
        
        if commits_count is not None and commits_count > 0:
            return f"- Pushed {commits_count} commits to {nome_repo}"
        else:
            return f"- Pushed to {nome_repo}"
    
    elif tipo_evento == 'CreateEvent':
        return f"- Created a new repo: {nome_repo}"
    
    elif tipo_evento == 'IssuesEvent' and event['payload'].get('action') == 'opened':
        return f"- Opened a new issue in {nome_repo}"
    
    elif tipo_evento == 'WatchEvent':
        return f"- Starred {nome_repo}"

    elif tipo_evento == 'DeleteEvent':
        return f"- Deleted {event['payload']['ref_type']} '{event['payload']['ref']}' from {nome_repo}"

    elif tipo_evento == 'ReleaseEvent':
        return f"- Published release {event['payload']['release']['tag_name']} for {nome_repo}"

    elif tipo_evento == 'MemberEvent':
        return f"- Was added as a collaborator to {nome_repo}"
    
    # ignora outros tipos de evento
    return None

def main():
    #  Lógica de Entrada do Usuário ---
    try:
        username = sys.argv[1]
    except IndexError:
        print("Erro: Você não digitou seu username!")
        print("Exemplo: python github_activity.py <username>")
        return # Sai da função

    print(f"--- Atividade Recente de: {username} ---")

    #  Lógica de Chamada da API e Erros ---
    try:
        # Chama nosso módulo de API 
        data_python = github_api.get_user_events(username)
        
        if not data_python:
            print("Nenhuma atividade recente encontrada.")
            return

        #  Lógica de Formatação e Saída ---
        for event in data_python:
            # Chama função de formatação
            output_string = format_event_string(event)
            # Só imprime se a função retornou uma string (e não None)
            if output_string:
                print(output_string)
    
    # Captura os erros personalizados que o 'github_api' pode lançar
    except github_api.UserNotFoundError:
        print(f"Erro: Usuário '{username}' não encontrado no GitHub.")
    except github_api.ApiError as e:
        # Captura todos os outros erros (conexão, etc.)
        print(f"Erro: Falha na comunicação com a API. Detalhes: {e}")

# --- Ponto de Entrada Padrão do Python ---
if __name__ == '__main__':
    main()