## 📊 **GitHub User Activity**

Script em Python para monitorar e processar a atividade de usuários no GitHub. O programa consome a API pública do GitHub para buscar eventos e os formata em uma lista legível, com lógica especial para `PushEvents` que conta o número exato de commits enviados.

---

### 🎯 Objetivo

Desenvolver um script Python que consome a API do GitHub para exibir a atividade de um usuário. O script foi projetado para atender aos seguintes requisitos:

* Conectar-se à API v1 do GitHub, enviando o `User-Agent` obrigatório.
* Buscar e listar os eventos recentes de um usuário específico.
* Identificar e processar **vários tipos de eventos** (como `PushEvent`, `CreateEvent`, `IssuesEvent`, `WatchEvent`, `DeleteEvent`, `ReleaseEvent` e `MemberEvent`), cada um com sua própria mensagem formatada.
* Para um `PushEvent`, realizar uma chamada de API aninhada (ao endpoint `/compare`) para determinar o **número exato de commits** enviados, em vez de apenas relatar o push.
* Otimizar o desempenho e evitar o esgotamento do limite da API usando um cache LRU (`Least Recently Used`).
* Aprimorar conhecimentos em consumo de APIs, manipulação de dados JSON, modularização de código e otimização com `functools`.

---

### 🗺️ Mapa interno dos arquivos

* **`github_activity.py`**: Arquivo principal (a "view") que contém a lógica de formatação de múltiplos eventos, consome o módulo de API e exibe a saída para o usuário.
* **`github_api.py`**: Módulo de serviço "privado". Contém toda a lógica de rede, incluindo a chamada principal à API (`_make_api_call`) e a função `get_commit_count`. É neste arquivo que o cache `@lru_cache` é implementado.
* **`.gitignore`**: Configurado para ignorar arquivos de cache do Python (`__pycache__`) e outros arquivos de ambiente.

---

### 📈 Funcionalidades

* **Formatação de Múltiplos Eventos:** Converte o feed JSON bruto da API em uma lista de strings legíveis, com formatação personalizada para:
    * `PushEvent` (Pushes)
    * `CreateEvent` (Criação de repositórios)
    * `IssuesEvent` (Abertura de Issues)
    * `WatchEvent` (Marcar repositórios com "Star")
    * `DeleteEvent` (Deleção de branches/tags)
    * `ReleaseEvent` (Publicação de Releases)
    * `MemberEvent` (Adição de colaboradores)
* **Contagem Detalhada de Commits:** Para `PushEvents`, o script faz uma segunda chamada de API para buscar o número exato de commits individuais dentro daquele push.
* **Cache Inteligente:** Utiliza o decorador `@lru_cache` do módulo `functools` para armazenar os resultados das chamadas de API. Isso evita requisições de rede repetidas para os mesmos dados, melhorando drasticamente a velocidade e respeitando os limites da API.
* **Tratamento de Erros:** Captura exceções personalizadas (como `ApiError`) para que o aplicativo não "quebre" se uma chamada de rede falhar, permitindo que ele continue processando outros eventos.

---

### 🛠 Tecnologias Utilizadas

(Bibliotecas nativas como `json`, `urllib` e `functools` foram usadas como parte do núcleo do Python.)

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git">
<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">

---

### 📂 Sugestões de melhorias / futuras implementações

* Adicionar formatação para ainda mais tipos de eventos que a API oferece (ex: `ForkEvent`, `PullRequestEvent`, `IssueCommentEvent`).
* Criar uma interface visual, seja uma página web simples (usando Flask/Django) ou uma GUI desktop (com Tkinter/PyQt), para exibir os resultados.
* Adicionar um sistema de autenticação (OAuth) para permitir que os usuários busquem atividades de seus repositórios privados e obtenham um limite de API maior.
* Implementar `asyncio` e `aiohttp` para fazer as chamadas de rede de forma assíncrona, melhorando ainda mais a performance.
