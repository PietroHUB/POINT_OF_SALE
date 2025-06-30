# caixa/middleware.py

from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from .license_validator import validar_licenca

# Guarda o estado da licença em memória para não verificar a cada requisição
LICENSE_INFO = None

def get_license_info():
    """Função para garantir que a validação ocorra apenas uma vez."""
    global LICENSE_INFO
    if LICENSE_INFO is None:
        LICENSE_INFO = validar_licenca()
    return LICENSE_INFO

class LicenseCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Força a primeira validação na inicialização do servidor
        get_license_info()

    def __call__(self, request):
        license_info = get_license_info()

        # Permite acesso irrestrito à página de licença e ao admin (para login/logout)
        # A lógica de bloqueio do admin será tratada de forma mais específica
        if request.path.startswith('/admin/login/') or request.path.startswith('/admin/logout/'):
             return self.get_response(request)

        # Bloqueio total e imediato para o painel de administração se a licença não for válida
        if request.path.startswith('/admin/'):
            if not license_info['valida']:
                # Você pode criar uma página HTML bonita para isso em vez de um simples texto
                return HttpResponseForbidden(
                    f"<h1>Acesso Bloqueado</h1>"
                    f"<p>O acesso ao painel administrativo está desativado.</p>"
                    f"<p><b>Motivo:</b> {license_info['mensagem']}</p>"
                    f"<p>Por favor, contate o suporte para regularizar sua licença.</p>"
                )

        # Bloqueio do sistema principal (PDV)
        # Aqui aplicamos a regra de tolerância. Vamos assumir que a trava é total
        # apenas se a licença expirou há mais de 15 dias (45 - 30).
        TOLERANCE_DAYS = -15 
        if not license_info['valida'] and license_info.get('dias_restantes', 0) < TOLERANCE_DAYS:
             return HttpResponseForbidden(
                    f"<h1>Sistema Bloqueado</h1>"
                    f"<p><b>Motivo:</b> {license_info['mensagem']}</p>"
                    f"<p>O período de tolerância para uso do sistema expirou. Por favor, contate o suporte.</p>"
                )

        response = self.get_response(request)
        return response
