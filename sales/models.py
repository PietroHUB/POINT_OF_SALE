from django.db import models
from products.models import Product
from caixa.models import PaymentMethod
from customers.models import Customer # Importa o novo modelo Customer
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class Sale(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT, # Evita excluir um cliente que tenha vendas associadas
        verbose_name=_("Cliente"),
        null=True, # Permite que a venda não tenha cliente (vendas à vista)
        blank=True,
        related_name='sales'
    )
    # O campo payment_method foi removido daqui.
    # O total_amount continua sendo o valor total dos produtos da venda.
    total_amount = models.DecimalField(
        _("Valor Total da Venda"),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    change_amount = models.DecimalField(
        _("Valor do Troco"),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_("Valor do troco devolvido ao cliente.")
    )
    created_at = models.DateTimeField(_("Data da Venda"), auto_now_add=True)
    # Adicione quaisquer outros campos que seu modelo Sale possa ter.

    class Meta:
        verbose_name = _("Venda")
        verbose_name_plural = _("Vendas")
        ordering = ['-created_at']

    def __str__(self):
        return f"Venda #{self.id} - R$ {self.total_amount}"

class SalePayment(models.Model):
    sale = models.ForeignKey(
        Sale,
        related_name='payments', # Para acessar os pagamentos a partir de uma instância de Sale (sale.payments.all())
        on_delete=models.CASCADE,
        verbose_name=_("Venda")
    )
    payment_method = models.ForeignKey(
        PaymentMethod, # Referencia o seu modelo de Formas de Pagamento
        on_delete=models.PROTECT, # Evita excluir uma forma de pagamento se ela estiver em uso
        verbose_name=_("Forma de Pagamento")
    )
    amount = models.DecimalField(
        _("Valor Pago"),
        max_digits=10,
        decimal_places=2
    )
    created_at = models.DateTimeField(_("Data do Pagamento"), auto_now_add=True)

    class Meta:
        verbose_name = _("Pagamento da Venda")
        verbose_name_plural = _("Pagamentos da Venda")
        ordering = ['created_at']

    def __str__(self):
        return f"Pagamento de R$ {self.amount} para Venda #{self.sale.id} via {self.payment_method.description}"

# Não se esqueça de criar e aplicar as migrações após essas alterações:
# python manage.py makemigrations sales
# python manage.py migrate



class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale,
        related_name='items', # Permite acessar os itens de uma venda como sale.items.all()
        on_delete=models.CASCADE, # Se a Venda for deletada, seus itens também serão
        verbose_name=_("Venda")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT, # Impede que um produto seja deletado se estiver em algum SaleItem
        verbose_name=_("Produto")
    )
    quantity = models.DecimalField(
        _("Quantidade"),
        max_digits=10, # Defina a precisão total desejada
        decimal_places=3, # Defina o número de casas decimais (ex: 3 para permitir 0.500 kg ou 1.25 unidades)
        help_text=_("Quantidade vendida deste produto (pode ser decimal).")
    )
    unit_price = models.DecimalField(
        _("Preço Unitário na Venda"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Preço do produto no momento da venda.")
    )
    subtotal = models.DecimalField(
        _("Subtotal do Item"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Subtotal para este item (quantidade * preço unitário).")
    )

    class Meta:
        verbose_name = _("Item da Venda")
        verbose_name_plural = _("Itens da Venda")

    def __str__(self):
        return f"{self.quantity}x {self.product.name} na Venda #{self.sale.id}"

    def save(self, *args, **kwargs):
        # Calcula o subtotal automaticamente para garantir consistência
        logger.debug("Preparando para salvar SaleItem. Produto: %s, Quantidade: %s", self.product.name if self.product else 'N/A', self.quantity)
        self.subtotal = self.quantity * self.unit_price # Sempre calcula o subtotal
        logger.debug("Subtotal do SaleItem definido/recalculado para: %s", self.subtotal)

        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            logger.info("Novo SaleItem para Venda #%s salvo no banco. Produto: %s, Subtotal: %s", self.sale.id, self.product.name, self.subtotal)
        else:
            logger.info("SaleItem para Venda #%s atualizado no banco.", self.sale.id)
