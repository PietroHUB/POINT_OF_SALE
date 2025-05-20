from django.shortcuts import render
from django.http import JsonResponse # Para retornar respostas JSON
from django.views.decorators.csrf import csrf_exempt # Para permitir requisições POST sem CSRF token (para API simples)
from django.views.decorators.http import require_POST # Para aceitar apenas requisições POST
import json # Para parsear o corpo da requisição JSON
from .models import Sale, SaleItem # Importar seus modelos de venda
from products.models import Product # Importar o modelo de produto
from decimal import Decimal # Para lidar com valores monetários com precisão

# Create your views here.

# View para a página principal do caixa (já existe no app caixa)
# from caixa.views import sales_page_view
import datetime
def agora():
    agora = datetime.datetime.now()
    agora = agora.strftime("%Y-%m-%d %H:%M:%S")
    return str(agora)

@csrf_exempt # Cuidado: Desabilita a proteção CSRF para esta view. Use com cautela em produção.
@require_POST # Garante que esta view só responda a requisições POST
def finalize_sale(request):
    print(f"{agora()} - {agora()} - CONSOLE (BACKEND): View finalize_sale chamada.")
    try:
        # 1. Receber e parsear os dados JSON da requisição
        data = json.loads(request.body)
        print(f"{agora()} - {agora()} - CONSOLE (BACKEND): Dados recebidos:", data)

        total_amount = Decimal(data.get('total_amount', 0))
        payment_method = data.get('payment_method', 'Desconhecido')
        items_data = data.get('items', [])

        if not items_data:
            print(f"{agora()} - {agora()} - CONSOLE (BACKEND): Nenhum item na venda. Abortando salvamento.")
            return JsonResponse({'status': 'error', 'message': 'Nenhum item na venda.'}, status=400)

        # 2. Criar a instância da Venda (Sale)
        sale = Sale(total_amount=total_amount, payment_method=payment_method)
        sale.save() # Salva a venda principal (isso disparará o print no modelo Sale)
        print(f"{agora()} - CONSOLE (BACKEND): Instância de Venda criada com ID: {sale.id}")

        # 3. Criar as instâncias dos Itens da Venda (SaleItem)
        for item_data in items_data:
            product_id = item_data.get('productId')
            quantity = item_data.get('quantity', 1)
            unit_price = Decimal(item_data.get('price', 0)) # Usar o preço unitário do frontend

            try:
                product = Product.objects.get(id=product_id)
                sale_item = SaleItem(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    # subtotal será calculado no save() do SaleItem se não for fornecido
                )
                sale_item.save() # Salva o item da venda (isso disparará o print no modelo SaleItem)
                print(f"{agora()} - CONSOLE (BACKEND): Instância de SaleItem criada para Produto ID {product_id}.")
            except Product.DoesNotExist:
                print(f"{agora()} - CONSOLE (BACKEND): Produto com ID {product_id} não encontrado. Ignorando item.")
                # Opcional: Você pode querer lidar com isso de forma mais robusta

        print(f"{agora()} - CONSOLE (BACKEND): Venda #{sale.id} e seus itens salvos com sucesso.")
        return JsonResponse({'status': 'success', 'sale_id': sale.id})

    except json.JSONDecodeError:
        print(f"{agora()} - {agora()} - CONSOLE (BACKEND): Erro ao parsear JSON.")
        return JsonResponse({'status': 'error', 'message': 'Requisição inválida (JSON inválido).'}, status=400)
    except Exception as e:
        print(f"{agora()} - CONSOLE (BACKEND): Erro interno ao finalizar venda: {e}")
        return JsonResponse({'status': 'error', 'message': f'Erro interno: {e}'}, status=500)
