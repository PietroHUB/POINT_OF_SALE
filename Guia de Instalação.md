# Guia de Instalação do Sistema PDV

Este guia detalha o processo completo para instalar e configurar o sistema de Ponto de Venda em uma nova máquina.

---

## 1. Pré-requisitos

Antes de começar, garanta que os seguintes programas estejam instalados na máquina:

*   **Python:** Versão 3.10 ou superior. Você pode baixá-lo em [python.org](https://www.python.org/downloads/).
    *   *Importante:* Durante a instalação do Python no Windows, marque a opção **"Add Python to PATH"**.
*   **Git:** Necessário para clonar o código-fonte do projeto. Baixe em [git-scm.com](https://git-scm.com/downloads).
*   **PostgreSQL:** O banco de dados utilizado pelo sistema. Baixe em [postgresql.org](https://www.postgresql.org/download/).

---

## 2. Configuração do Banco de Dados

O sistema precisa de um banco de dados e um usuário para operar.

1.  **Abra o psql (terminal do PostgreSQL) ou o pgAdmin.**
2.  **Crie um novo banco de dados.** Substitua `nome_do_banco` pelo nome que preferir.
    ```sql
    CREATE DATABASE nome_do_banco;
    ```
3.  **Crie um novo usuário e uma senha para ele.** Substitua `nome_do_usuario` e `senha_forte` pelos seus dados.
    ```sql
    CREATE USER nome_do_usuario WITH PASSWORD 'senha_forte';
    ```
4.  **Conceda todas as permissões do banco de dados ao novo usuário.**
    ```sql
    GRANT ALL PRIVILEGES ON DATABASE nome_do_banco TO nome_do_usuario;
    ```
5.  **Anote o nome do banco, o nome de usuário e a senha.** Você precisará deles em breve.

---

## 3. Instalação do Projeto

Siga estes passos para configurar o código-fonte do projeto.

1.  **Clone o repositório:**
    Abra um terminal (Prompt de Comando, PowerShell ou Terminal) e execute o comando abaixo para baixar o projeto.
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO_GIT> POINT_OF_SALE
    cd POINT_OF_SALE
    ```
    *(Se você estiver apenas copiando os arquivos, simplesmente navegue até a pasta do projeto pelo terminal.)*

2.  **Crie e ative o ambiente virtual:**
    Este passo isola as dependências do projeto.
    ```bash
    # Cria o ambiente virtual
    python -m venv venv

    # Ativa o ambiente (Windows)
    .\venv\Scripts\activate

    # Ativa o ambiente (macOS/Linux)
    source venv/bin/activate
    ```
    *Você saberá que funcionou se o nome `(venv)` aparecer no início da linha do seu terminal.*

3.  **Instale as dependências do Python:**
    Este comando instala o Django e todas as outras bibliotecas necessárias.
    ```bash
    pip install -r requirements.txt
    ```

---

## 4. Configuração do Sistema

Agora, vamos conectar o projeto ao banco de dados que você criou.

1.  **Abra o arquivo `pos_project/settings.py`** em um editor de texto.
2.  **Localize a seção `DATABASES`**.
3.  **Edite os campos** com os dados do banco de dados que você anotou no Passo 2.
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'nome_do_banco',      # <-- Substitua aqui
            'USER': 'nome_do_usuario',   # <-- Substitua aqui
            'PASSWORD': 'senha_forte',   # <-- Substitua aqui
            'HOST': '127.0.0.1',         # Geralmente não precisa mudar
            'PORT': '5432',              # Geralmente não precisa mudar
        }
    }
    ```
4.  **Salve e feche o arquivo.**

---

## 5. Inicialização e Execução

Os passos finais para colocar o sistema no ar.

1.  **Aplique as migrações do banco de dados:**
    Este comando cria todas as tabelas necessárias no banco de dados.
    ```bash
    python manage.py migrate
    ```

2.  **Crie um superusuário:**
    Este será o seu usuário administrador para acessar o painel `/admin`.
    ```bash
    python manage.py createsuperuser
    ```
    *Siga as instruções para definir um nome de usuário, e-mail e senha.*

3.  **Ative a Licença do Software:**
    *   Obtenha a chave de licença (o texto que começa com `PLIMA-...`) com o desenvolvedor.
    *   Na pasta raiz do projeto, crie um arquivo de texto chamado `license.key`.
    *   Cole a chave de licença dentro deste arquivo e salve.

4.  **Inicie o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

## 6. Verificação Final

Se tudo correu bem, o servidor estará rodando.

1.  Abra seu navegador e acesse [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Você deve ver a tela de seleção de caixa.
2.  Acesse [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) e faça login com o superusuário que você criou.
3.  Acesse [http://127.0.0.1:8000/ativacao/](http://127.0.0.1:8000/ativacao/) para verificar o status da sua licença.

**A instalação está concluída!**
