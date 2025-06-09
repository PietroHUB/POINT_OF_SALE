from django.shortcuts import render
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST 
import json 
from .models import Sale, SaleItem
from products.models import Product 
from decimal import Decimal 
from django.db import transaction 
import logging 

logger = logging.getLogger(__name__) 

"""

novo server:

localhost
5432
user: postgres
password: 123456

novo banco de dados:
point_of_sale_db

fiz python manage.py createsuperuser

login: pvplima
senha: joao@316


cd c:\Pietro\Projetos\POINT_OF_SALE\
.\venv\Scripts\activate
python manage.py runserver
http://127.0.0.1:8000/

http://localhost:8000/admin/


"""


@csrf_exempt 
@require_POST 
def finalize_sale(request):
    logger.info("View finalize_sale chamada.")
    try:
        # 1. Receber e parsear os dados JSON da requisição
        data = json.loads(request.body)
        logger.debug("Dados recebidos: %s", data)

        # Validação básica dos dados recebidos
        payment_method = data.get('payment_method', 'Desconhecido')
        items_data = data.get('items', [])

        if not items_data:
            logger.warning("Nenhum item na venda. Abortando salvamento.")
            return JsonResponse({'status': 'error', 'message': 'Nenhum item na venda.'}, status=400)
        
        # Usar uma transação atômica para garantir que a venda e todos os itens sejam salvos ou nenhum seja.
        with transaction.atomic():
            # 2. Criar a instância da Venda (Sale) - O total_amount será calculado com base nos itens.
            sale = Sale(payment_method=payment_method, total_amount=Decimal('0.00')) # Inicializa com 0.00
            sale.save() # Salva a venda principal para obter um ID
            logger.info("Instância de Venda #%s criada (total inicial 0.00).", sale.id)

            calculated_total = Decimal('0.00')

            # 3. Criar as instâncias dos Itens da Venda (SaleItem)
            for item_data in items_data:
                product_id = item_data.get('productId')
                quantity_str = item_data.get('quantity')
                unit_price_str = item_data.get('price')

                # Validação mais detalhada do item
                if product_id is None or quantity_str is None or unit_price_str is None:
                    logger.error("Dados incompletos para o item: %s. Abortando venda.", item_data)
                    # transaction.atomic() fará o rollback da 'sale' já salva.
                    return JsonResponse({'status': 'error', 'message': f'Dados incompletos para o item: {item_data}. productId, quantity e price são obrigatórios.'}, status=400)

                try:
                    quantity = int(quantity_str)
                    unit_price = Decimal(str(unit_price_str)) # Converter para string primeiro evita problemas de precisão com floats
                except (ValueError, TypeError):
                    logger.error("Quantidade ou preço inválido para o item: %s. Abortando venda.", item_data)
                    return JsonResponse({'status': 'error', 'message': f'Quantidade ou preço inválido para o item {item_data}. Devem ser números válidos.'}, status=400)

                if quantity <= 0:
                    logger.error("Quantidade deve ser positiva para o item: %s. Abortando venda.", item_data)
                    return JsonResponse({'status': 'error', 'message': f'Quantidade deve ser maior que zero para o produto ID {product_id}.'}, status=400)
                
                if unit_price < 0: # Permitindo preço zero (ex: item promocional)
                    logger.error("Preço unitário não pode ser negativo para o item: %s. Abortando venda.", item_data)
                    return JsonResponse({'status': 'error', 'message': f'Preço unitário não pode ser negativo para o produto ID {product_id}.'}, status=400)

                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    logger.error("Produto com ID %s não encontrado. Abortando venda.", product_id)
                    return JsonResponse({'status': 'error', 'message': f'Produto com ID {product_id} não encontrado.'}, status=400)
                
                # Verificar estoque
                if product.stock_quantity < quantity:
                    logger.error("Estoque insuficiente para Produto ID %s. Solicitado: %s, Disponível: %s. Abortando venda.", product_id, quantity, product.stock_quantity)
                    return JsonResponse({
                        'status': 'error', 
                        'message': f'Estoque insuficiente para o produto "{product.name}" (ID {product_id}). Solicitado: {quantity}, Disponível: {product.stock_quantity}.'
                    }, status=400) # HTTP 400 ou 409 (Conflict) podem ser apropriados

                sale_item = SaleItem(
                                        sale=sale, 
                                        product=product, 
                                        quantity=quantity, 
                                        unit_price=unit_price
                                    )
                sale_item.save() # Salva o item da venda (subtotal será calculado no save() do SaleItem)
                calculated_total += sale_item.subtotal # Soma ao total calculado

                # Deduzir do estoque
                product.stock_quantity -= quantity
                product.save(update_fields=['stock_quantity'])
                logger.info("Estoque do Produto ID %s atualizado para %s.", product.id, product.stock_quantity)
                logger.debug("SaleItem para Produto ID %s salvo. Subtotal: %s.", product_id, sale_item.subtotal)
                            
            # 4. Atualizar o total_amount na Venda principal com base nos itens
            sale.total_amount = calculated_total
            sale.save(update_fields=['total_amount']) 
            logger.info("Total da venda #%s calculado e salvo: %s", sale.id, calculated_total)

            # Log final da venda
            logger.info("Venda #%s e seus itens salvos com sucesso. Total: %s, Pagamento: %s", sale.id, calculated_total, sale.payment_method)

        return JsonResponse({'status': 'success', 'sale_id': sale.id})

    except json.JSONDecodeError:
        logger.error("Erro ao parsear JSON na requisição.", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'Requisição inválida (JSON inválido).'}, status=400)
    except Exception as e:
        logger.exception("Erro interno ao finalizar venda:") # Loga a exceção completa
        return JsonResponse({'status': 'error', 'message': f'Erro interno: {e}'}, status=500)
