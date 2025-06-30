# caixa/license_validator.py

import jwt
from django.conf import settings
from datetime import datetime
import os

# Define o caminho para o arquivo de licença na raiz do projeto
LICENSE_FILE_PATH = os.path.join(settings.BASE_DIR, 'license.key')

def get_license_key_from_file():
    """Lê a chave de licença do arquivo license.key."""
    try:
        with open(LICENSE_FILE_PATH, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "" # Retorna uma string vazia se o arquivo não existir

def validar_licenca():
    """
    Verifica a licença lida do arquivo license.key.
    Retorna um dicionário com o status da validação.
    """
    license_key = get_license_key_from_file()
    if not license_key:
        return {'valida': False, 'dias_restantes': 0, 'mensagem': "Arquivo de licença 'license.key' não encontrado ou vazio."}

    try:
        # Remove o prefixo "PLIMA-" antes de decodificar
        token = license_key.replace("PLIMA-", "")

        # Decodifica o token usando a mesma chave secreta
        payload = jwt.decode(
            token, 
            settings.LICENSE_SECRET_KEY, 
            algorithms=["HS256"]
        )
        
        # Se chegou aqui, a licença é autêntica. Agora, verificamos a validade.
        data_expiracao = datetime.fromtimestamp(payload['exp'])
        dias_restantes = (data_expiracao - datetime.now()).days

        if dias_restantes < 0:
            return {
                'valida': False,
                'dias_restantes': dias_restantes,
                'cliente': payload.get('cliente', 'N/A'),
                'mensagem': f"Licença expirada há {-dias_restantes} dia(s)."
            }

        return {
            'valida': True,
            'dias_restantes': dias_restantes,
            'cliente': payload.get('cliente', 'N/A'),
            'mensagem': f"Licença válida. Restam {dias_restantes} dia(s)."
        }

    except jwt.ExpiredSignatureError:
        return {'valida': False, 'dias_restantes': 0, 'mensagem': "Licença expirada!"}
    except (jwt.InvalidTokenError, AttributeError):
        return {'valida': False, 'dias_restantes': 0, 'mensagem': "Chave de licença inválida."}
