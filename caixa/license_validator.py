# caixa/license_validator.py

import jwt
from django.conf import settings
from datetime import datetime

def validar_licenca():
    """
    Verifica a licença do settings.py.
    Retorna um dicionário com o status da validação.
    """
    try:
        # Remove o prefixo "PLIMA-" antes de decodificar
        license_key = settings.LICENSE_KEY.replace("PLIMA-", "")

        # Decodifica o token usando a mesma chave secreta
        payload = jwt.decode(
            license_key, 
            settings.LICENSE_SECRET_KEY, 
            algorithms=["HS256"]
        )
        
        # Se chegou aqui, a licença é autêntica. Agora, verificamos a validade.
        data_expiracao = datetime.fromtimestamp(payload['exp'])
        dias_restantes = (data_expiracao - datetime.now()).days

        if dias_restantes < 0:
            # Trata o caso de a licença ter expirado há alguns dias
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
        # A licença expirou
        return {'valida': False, 'dias_restantes': 0, 'mensagem': "Licença expirada!"}
    except (jwt.InvalidTokenError, AttributeError):
        # A licença é inválida, mal formatada, não existe no settings, ou a assinatura não confere
        return {'valida': False, 'dias_restantes': 0, 'mensagem': "Chave de licença inválida ou não configurada."}
