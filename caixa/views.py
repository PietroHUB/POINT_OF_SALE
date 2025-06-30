from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import PaymentMethod, PointOfSale
from .license_validator import validar_licenca, get_license_key_from_file, LICENSE_FILE_PATH

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

def license_activation_view(request):
    """
    Página para o cliente inserir e ativar uma nova chave de licença.
    """
    if request.method == 'POST':
        new_key = request.POST.get('license_key', '').strip()
        if new_key:
            try:
                with open(LICENSE_FILE_PATH, 'w') as f:
                    f.write(new_key)
                messages.success(request, 'Chave de licença atualizada com sucesso! Por favor, reinicie o servidor para que a nova licença seja ativada.')
            except IOError as e:
                messages.error(request, f'Erro ao salvar a chave de licença: {e}')
        else:
            messages.warning(request, 'O campo da chave de licença não pode estar vazio.')
        
        return redirect('caixa:license_activation')

    # Para requisições GET
    license_info = validar_licenca()
    current_key = get_license_key_from_file()
    
    context = {
        'page_title': 'Ativação de Licença',
        'license_info': license_info,
        'current_key': current_key
    }
    return render(request, 'caixa/license_activation_page.html', context)
