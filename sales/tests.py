from django.test import TestCase, Client
from django.urls import reverse
import json
from decimal import Decimal
from products.models import Product 
from .models import Sale, SaleItem

#para usar a test rode o seguinte comando no prompt:
#python manage.py test sales

class FinalizeSaleViewTests(TestCase):
    def setUp(self):
        # Configurações iniciais para os testes
        self.client = Client()
        self.finalize_url = reverse('sales:finalize_sale') # Usa o namespace 'sales'

        # Cria alguns produtos de teste no banco de dados
        self.product1 = Product.objects.create(name="Produto A", price=Decimal('10.50'), stock=100)
        self.product2 = Product.objects.create(name="Produto B", price=Decimal('5.00'), stock=50)

    def test_finalize_sale_success(self):
        """Testa a finalização de uma venda com sucesso."""
        payload = {
            'payment_method': 'Cartão de Crédito',
            'items': [
                {'productId': self.product1.id, 'quantity': 2, 'price': '10.50'}, # Preço como string para simular JSON
                {'productId': self.product2.id, 'quantity': 3, 'price': '5.00'},
            ]
        }
        # O total_amount no payload não é usado pela view após a mudança,
        # mas pode ser enviado pelo frontend. Vamos omitir para testar a lógica do backend.

        response = self.client.post(self.finalize_url, json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'success')
        self.assertIn('sale_id', response_data)

        # Verifica se a venda e os itens foram criados no banco
        sale = Sale.objects.get(id=response_data['sale_id'])
        self.assertEqual(sale.payment_method, 'Cartão de Crédito')
        # Verifica se o total calculado no backend está correto (2*10.50 + 3*5.00 = 21.00 + 15.00 = 36.00)
        self.assertEqual(sale.total_amount, Decimal('36.00'))

        sale_items = sale.items.all()
        self.assertEqual(sale_items.count(), 2)

        # Verifica os detalhes dos itens (ordem pode variar, então verificamos por produto)
        item1 = sale_items.get(product=self.product1)
        self.assertEqual(item1.quantity, 2)
        self.assertEqual(item1.unit_price, Decimal('10.50'))
        self.assertEqual(item1.subtotal, Decimal('21.00'))

        item2 = sale_items.get(product=self.product2)
        self.assertEqual(item2.quantity, 3)
        self.assertEqual(item2.unit_price, Decimal('5.00'))
        self.assertEqual(item2.subtotal, Decimal('15.00'))

    def test_finalize_sale_no_items(self):
        """Testa a finalização de uma venda sem itens."""
        payload = {
            'payment_method': 'Dinheiro',
            'items': []
        }

        response = self.client.post(self.finalize_url, json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'error')
        self.assertIn('Nenhum item na venda.', response_data['message'])
        self.assertEqual(Sale.objects.count(), 0) # Nenhuma venda deve ser criada

    def test_finalize_sale_invalid_json(self):
        """Testa a finalização de uma venda com JSON inválido."""
        invalid_payload = "isto não é um json válido"

        response = self.client.post(self.finalize_url, invalid_payload, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'error')
        self.assertIn('JSON inválido', response_data['message'])
        self.assertEqual(Sale.objects.count(), 0) # Nenhuma venda deve ser criada

    # TODO: Adicionar mais testes:
    # - Produto inexistente
    # - Quantidade ou preço inválido (negativo, zero, não numérico)
    # - Payload com estrutura inesperada (ex: 'items' não é lista)
    # - Testar com diferentes formas de pagamento
    # - Testar transação atômica (simular falha ao salvar um item)

class SaleModelTests(TestCase):
    def test_sale_item_subtotal_calculation(self):
        """Testa se o subtotal do SaleItem é calculado corretamente ao salvar."""
        product = Product.objects.create(name="Produto Teste", price=Decimal('25.00'), stock=10)
        sale = Sale.objects.create(total_amount=Decimal('0.00'), payment_method='Teste')

        item = SaleItem(sale=sale, product=product, quantity=4, unit_price=Decimal('25.00'))
        item.save()

        self.assertEqual(item.subtotal, Decimal('100.00'))

    # TODO: Adicionar mais testes para os modelos
    # - Testar o __str__ dos modelos
    # - Testar o ordering na Meta da Sale
