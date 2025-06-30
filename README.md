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

## Guia Prático de Ativação e Renovação de Licença

Este guia descreve o processo de geração de uma nova chave pelo desenvolvedor e a ativação pelo cliente final através da página de licença do sistema.

### Parte 1: Geração da Chave (Para o Desenvolvedor)

Utilize o script `gerador_de_chaves.py` que está na raiz do projeto. Este script **não deve ser distribuído** para o cliente.

1.  Abra um terminal na raiz do projeto.
2.  Execute o script:
    ```bash
    python gerador_de_chaves.py
    ```
3.  O script irá gerar e imprimir uma nova chave de licença válida por 30 dias.
4.  Copie a chave completa (iniciada com `PLIMA-...`) e envie-a para o seu cliente.

### Parte 2: Instalação da Chave (Para o Cliente)

O cliente final deve seguir estes passos para ativar ou renovar a licença do sistema:

1.  Abra o navegador e acesse a **Página de Ativação de Licença** do sistema. Geralmente, o endereço é:
    `http://localhost:8000/ativacao/`

2.  Na página, ele verá o status da licença atual (se está válida, expirada ou inválida).

3.  No campo "Nova Chave de Licença", ele deve colar a chave completa que você forneceu.

4.  Clique no botão **"Salvar Nova Chave"**.

### Parte 3: Reinicializaç��o do Sistema

Para que a nova licença seja validada, o servidor do sistema precisa ser **reiniciado**.

Após a reinicialização, a nova licença estará ativa, e o sistema voltará a funcionar normalmente pelo período de validade da chave. A página de ativação mostrará o novo status e os dias restantes.


