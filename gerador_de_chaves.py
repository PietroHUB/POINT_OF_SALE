# gerador_de_chaves.py
import jwt
from datetime import datetime, timedelta

# !! IMPORTANTE !!
# Esta chave secreta DEVE ser a mesma que está no settings.py do seu cliente.
SECRET_KEY = "plima-secret-key-for-jwt-signature-2024"

def gerar_licenca(dias_de_validade, cliente_id):
    """
    Gera uma chave de licença (token JWT) com data de validade e prefixo.
    """
    # Calcula a data de expiração
    data_expiracao = datetime.utcnow() + timedelta(days=dias_de_validade)
    
    payload = {
        'exp': data_expiracao,  # Data de expiração (padrão do JWT)
        'iat': datetime.utcnow(), # Data de emissão
        'cliente': cliente_id   # Identificador do cliente
    }
    
    # Gera o token usando o algoritmo HS256
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    # Adiciona o prefixo
    return f"PLIMA-{token}"

# --- Como usar ---
if __name__ == "__main__":
    # Gerar uma licença para o "Cliente Padrão" com validade de 30 dias
    dias = 30
    cliente = "Cliente Padrão"
    
    chave_licenca = gerar_licenca(dias_de_validade=dias, cliente_id=cliente)
    
    print("--- SUA NOVA CHAVE DE LICENÇA ---")
    print(f"Cliente: {cliente}")
    print(f"Validade: {dias} dias")
    print("\nCopie a chave abaixo e cole no arquivo 'pos_project/settings.py', na variável LICENSE_KEY.")
    print("-" * 35)
    print(chave_licenca)
    print("-" * 35)

