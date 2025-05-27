from django.shortcuts import render
from django.contrib.auth.decorators import login_required # Para proteger a página
from products.models import Product # Correto: Product vem do app 'products'
from .models import PaymentMethod # Correto: PaymentMethod vem deste app 'caixa'
from django.http import HttpResponse # Importe HttpResponse se necessário, mas render já retorna um

"""

Explicação:

sales_page_view: Esta função será chamada quando um usuário acessar a URL da página de vendas.

@login_required: (Comentado por enquanto) 
Este decorador garante que apenas usuários logados no sistema Django possam acessar esta página.

Product.objects.all(): Busca todos os produtos cadastrados no banco de dados.

context: Um dicionário que passa dados para o template.

render(request, 'caixa/sales_page.html', context): Renderiza o template HTML que vamos criar a seguir.

"""
# @login_required # Descomente se quiser que apenas usuários logados acessem
def sales_page_view(request):
    products = Product.objects.all().order_by('name') # Pega todos os produtos ordenados por nome
    """
        select 
            * 
        from products_product
    """

    payment_methods = PaymentMethod.objects.all().order_by('id')

    context = {
        'products': products,
        'page_title': 'Ponto de Venda',
        'payment_methods': payment_methods,
    }
    return render(request, 'caixa/sales_page.html', context)