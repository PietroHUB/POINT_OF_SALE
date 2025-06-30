# POINT_OF_SALE

Este é um sistema de Ponto de Venda (PDV) desenvolvido em Django, projetado para ser robusto, rápido e fácil de usar em ambientes de varejo.

## Configuração do Ambiente de Desenvolvimento

Para garantir que o projeto funcione corretamente, todas as dependências devem ser instaladas dentro de um ambiente virtual (`venv`).

1.  **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

2.  **Instale as dependências:**
    O arquivo `requirements.txt` contém todas as bibliotecas necessárias. Para instalar ou atualizar, execute:
    ```bash
    pip install -r requirements.txt
    ```

## Sistema de Licenciamento Offline

Para garantir a proteção contra o uso não autorizado e, ao mesmo tempo, permitir que o sistema funcione em estabelecimentos sem acesso constante à internet, foi implementado um sistema de licenciamento offline baseado em chaves de ativação com prazo de validade.

### Como Funciona

O sistema utiliza **JSON Web Tokens (JWT)** assinados com o algoritmo **HS256** para gerar e validar as chaves de licença. Este método não criptografa os dados da licença, mas os assina digitalmente, garantindo:

1.  **Autenticidade:** Apenas o desenvolvedor, que possui a chave secreta (`LICENSE_SECRET_KEY`), pode gerar uma licença válida.
2.  **Integridade:** Qualquer tentativa de alterar o conteúdo da licença (como a data de validade) invalidará a assinatura digital, bloqueando o sistema.
3.  **Funcionamento Offline:** A validação da licença é feita localmente, usando a data e hora do sistema, sem a necessidade de conexão com a internet.

---

## Guia Prático: Gerando e Instalando uma Nova Chave de Licença

Este guia destina-se ao desenvolvedor para a geração de chaves para novos clientes ou para renovação.

### Passo 1: Gerar a Chave

Utilize o script `gerador_de_chaves.py` que está na raiz do projeto. Este script **não deve ser distribuído** para o cliente.

1.  Abra um terminal na raiz do projeto.
2.  Execute o script:
    ```bash
    python gerador_de_chaves.py
    ```
3.  O script irá imprimir no terminal uma nova chave de licença válida por 30 dias. A saída será parecida com esta:

    ```
    --- SUA NOVA CHAVE DE LICENÇA ---
    Cliente: Cliente Padrão
    Validade: 30 dias

    Copie a chave abaixo e cole no arquivo 'pos_project/settings.py', na variável LICENSE_KEY.
    -----------------------------------
    PLIMA-eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTM5ODg0MDAsIm...
    -----------------------------------
    ```

### Passo 2: Instalar a Chave no Sistema do Cliente

1.  Copie a chave completa gerada pelo script (incluindo o prefixo `PLIMA-`).
2.  Abra o arquivo de configuração do projeto do cliente: `pos_project/settings.py`.
3.  Localize a variável `LICENSE_KEY`.
4.  Cole a nova chave como o valor da variável, substituindo a antiga. O resultado deve ser:
    ```python
    # pos_project/settings.py

    # ... outras configurações ...

    LICENSE_KEY = "PLIMA-eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTM5ODg0MDAsIm..."
    ```

5.  Salve o arquivo `settings.py`.

### Passo 3: Reiniciar o Servidor

Para que a nova licença seja lida e validada, o servidor Django precisa ser reiniciado. Após a reinicialização, o sistema estará desbloqueado e funcional pelo período de validade da nova chave.


