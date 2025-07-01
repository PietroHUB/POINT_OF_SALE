from django.shortcuts import render
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST 
import json 
from .models import Sale, SaleItem, SalePayment
from products.models import Product
from caixa.models import PaymentMethod, PointOfSale
from customers.models import Customer # Adicionado
from decimal import Decimal, InvalidOperation
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


class SaleValidationError(Exception):
    """Exceção customizada para erros de validação da venda."""
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

@csrf_exempt 
@require_POST 
def finalize_sale(request):
    logger.info("View finalize_sale chamada.")
    try:
        data = json.loads(request.body)
        logger.debug("Dados recebidos: %s", data)

        items_data = data.get('items', [])
        payments_data = data.get('payments', [])
        customer_id = data.get('customer_id')
        point_of_sale_id = data.get('point_of_sale_id') # Novo

        if not all([items_data, payments_data, point_of_sale_id]):
            raise SaleValidationError("Dados de itens, pagamento ou ponto de venda faltando.", status_code=400)

        with transaction.atomic():
            # --- 1. Valida e busca o cliente e o POS ---
            pos_instance = PointOfSale.objects.get(id=point_of_sale_id)
            customer_instance = None
            if customer_id:
                try:
                    customer_instance = Customer.objects.get(id=customer_id)
                except Customer.DoesNotExist:
                    raise SaleValidationError(f"Cliente com ID {customer_id} não encontrado.")

            # --- 2. Cria a venda inicial ---
            sale = Sale.objects.create(
                customer=customer_instance,
                point_of_sale=pos_instance
            )
            logger.info("Venda #%s criada para o cliente: %s no POS: %s", sale.id, customer_instance, pos_instance)

            # --- 3. Processa os itens da venda ---
            calculated_total = Decimal('0.00')
            for item_data in items_data:
                product = Product.objects.get(id=item_data.get('productId'))
                quantity = Decimal(item_data.get('quantity'))
                
                if product.stock_quantity < quantity:
                    raise SaleValidationError(f'Estoque insuficiente para "{product.name}".')

                sale_item = SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    unit_price=Decimal(item_data.get('price'))
                )
                calculated_total += sale_item.subtotal
                product.stock_quantity -= quantity
                product.save()

            # --- 4. Atualiza o total da venda ---
            sale.total_amount = calculated_total
            sale.save()

            # --- 5. Processa os pagamentos ---
            total_paid = Decimal('0.00')
            for payment_data in payments_data:
                payment_method = PaymentMethod.objects.get(id=payment_data.get('payment_method_id'))
                amount = Decimal(payment_data.get('amount'))
                SalePayment.objects.create(sale=sale, payment_method=payment_method, amount=amount)
                total_paid += amount

            # --- 6. Valida o total pago e calcula o troco ---
            if total_paid < sale.total_amount:
                raise SaleValidationError(f"Pagamento (R$ {total_paid}) insuficiente para o total (R$ {sale.total_amount}).")
            
            sale.change_amount = total_paid - sale.total_amount
            sale.save()

            logger.info("Venda #%s finalizada com sucesso. Total: %s, Troco: %s", sale.id, sale.total_amount, sale.change_amount)

        # --- 7. Prepara os dados de retorno para o cupom ---
            sale_details = {
                'id': sale.id,
                'date': sale.created_at.strftime('%d/%m/%Y %H:%M:%S'),
                'customer': customer_instance.name if customer_instance else 'Consumidor Padrão',
                'items': [{
                    'name': item.product.name,
                    'quantity': f"{item.quantity:.2f}".replace('.', ','),
                    'unit_price': f"{item.unit_price:.2f}".replace('.', ','),
                    'subtotal': f"{item.subtotal:.2f}".replace('.', ',')
                } for item in sale.items.all()],
                'payments': [{
                    'method': p.payment_method.description,
                    'amount': f"{p.amount:.2f}".replace('.', ',')
                } for p in sale.payments.all()],
                'total_amount': f"{sale.total_amount:.2f}".replace('.', ','),
                'total_paid': f"{total_paid:.2f}".replace('.', ','),
                'change_amount': f"{sale.change_amount:.2f}".replace('.', ',')
            }

            logger.info("Venda #%s finalizada com sucesso. Total: %s, Troco: %s", sale.id, sale.total_amount, sale.change_amount)

        return JsonResponse({'status': 'success', 'sale_id': sale.id, 'sale_details': sale_details})

    except SaleValidationError as e:
        logger.warning("Erro de validação da venda: %s", e.message)
        return JsonResponse({'status': 'error', 'message': e.message}, status=e.status_code)
    except json.JSONDecodeError:
        logger.error("Erro de JSON na requisição.", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'JSON inválido.'}, status=400)
    except Exception as e:
        logger.exception("Erro interno inesperado ao finalizar venda:")
        return JsonResponse({'status': 'error', 'message': f'Erro interno: {str(e)}'}, status=500)
