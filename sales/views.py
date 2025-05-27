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
            # 2. Criar a instância da Venda (Sale)
            # O total_amount será calculado com base nos itens, não confiando no frontend.
            sale = Sale(payment_method=payment_method, total_amount=Decimal('0.00')) # Inicializa com 0.00
            sale.save() # Salva a venda principal para obter um ID
            logger.info("Instância de Venda criada com ID: %s", sale.id)

            calculated_total = Decimal('0.00')

            # 3. Criar as instâncias dos Itens da Venda (SaleItem)
            for item_data in items_data:
                product_id = item_data.get('productId')
                quantity = item_data.get('quantity') # Não usar default, validar se existe
                unit_price = item_data.get('price') # Não usar default, validar se existe

                # Validação mais detalhada do item
                if product_id is None or quantity is None or unit_price is None:
                    logger.warning("Dados de item inválidos: %s. Ignorando item.", item_data)
                    continue # Ignora item mal formatado

                try:
                    product = Product.objects.get(id=product_id)
                    quantity = int(quantity) # Tenta converter para int
                    unit_price = Decimal(str(unit_price)) # Tenta converter para Decimal (converter para string primeiro evita problemas de precisão com floats)

                    if quantity <= 0 or unit_price < 0:
                         logger.warning("Quantidade ou preço inválido para Produto ID %s. Ignorando item.", product_id)
                         continue

                    sale_item = SaleItem(
                                            sale=sale, 
                                            product=product, 
                                            quantity=quantity, 
                                            unit_price=unit_price
                                        )
                    sale_item.save() # Salva o item da venda (subtotal será calculado no save())
                    calculated_total += sale_item.subtotal # Soma ao total calculado
                    logger.debug("Instância de SaleItem criada para Produto ID %s.", product_id)
                except (Product.DoesNotExist, ValueError, TypeError) as e:
                    logger.error("Erro ao processar item (Produto ID %s): %s. Ignorando item.", product_id, e)
                    # Opcional: Você pode querer retornar um erro 400 se um produto não for encontrado ou dados forem inválidos

            # 4. Atualizar o total_amount na Venda principal
            sale.total_amount = calculated_total
            sale.save(update_fields=['total_amount']) # Salva apenas o campo total_amount
            logger.info("Venda #%s e seus itens salvos com sucesso. Total calculado: %s", sale.id, calculated_total)

        return JsonResponse({'status': 'success', 'sale_id': sale.id})

    except json.JSONDecodeError:
        logger.error("Erro ao parsear JSON na requisição.", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'Requisição inválida (JSON inválido).'}, status=400)
    except Exception as e:
        logger.exception("Erro interno ao finalizar venda:") # Loga a exceção completa
        return JsonResponse({'status': 'error', 'message': f'Erro interno: {e}'}, status=500)
