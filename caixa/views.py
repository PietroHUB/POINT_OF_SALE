from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import PaymentMethod, PointOfSale

#@login_required
def select_pos_view(request):
    """
    Exibe a tela para o operador selecionar em qual Ponto de Venda (POS) ele está.
    """
    points_of_sale = PointOfSale.objects.filter(is_active=True)
    context = {
        'points_of_sale': points_of_sale,
        'page_title': 'Selecionar Ponto de Venda'
    }
    return render(request, 'caixa/select_pos_page.html', context)

# @login_required
def sales_page_view(request, pos_id):
    """
    Página principal de vendas (PDV), agora ciente de qual POS está sendo usado.
    """
    point_of_sale = get_object_or_404(PointOfSale, id=pos_id)
    products = Product.objects.all().order_by('name')
    payment_methods = PaymentMethod.objects.all().order_by('id')

    context = {
        'products': products,
        'payment_methods': payment_methods,
        'point_of_sale': point_of_sale, # Passa o objeto POS para o template
        'page_title': f'Ponto de Venda - {point_of_sale.name}',
    }
    return render(request, 'caixa/sales_page.html', context)
