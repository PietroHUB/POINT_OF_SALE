from django.db import models
from django.conf import settings # Para referenciar o User model
from products.models import Product # Importar o modelo Product do seu app products
from django.utils.translation import gettext_lazy as _

import logging
logger = logging.getLogger(__name__)

class Sale(models.Model):
    # Opcional: Se você tiver login de operador de caixa
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.SET_NULL, # Se o usuário for deletado, a venda não é, mas o campo user fica null
    #     null=True,
    #     blank=True,
    #     verbose_name=_("Operador")
    # )
    total_amount = models.DecimalField(
        _("Valor Total"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Valor total da venda.")
    )
    payment_method = models.CharField(
        _("Forma de Pagamento"),
        max_length=50,
        default="Desconhecido", # Adicionar um default para migrações
        help_text=_("Forma de pagamento utilizada (Ex: Pix, Dinheiro, Cartão de Crédito).")
    )
    created_at = models.DateTimeField(
        _("Data e Hora da Venda"),
        auto_now_add=True, # Define automaticamente a data e hora na criação
        editable=False
    )

    class Meta:
        verbose_name = _("Venda")
        verbose_name_plural = _("Vendas")
        ordering = ['-created_at'] # Ordenar as vendas da mais recente para a mais antiga

    def __str__(self):
        return f"Venda #{self.id} - R$ {self.total_amount} ({self.created_at.strftime('%d/%m/%Y %H:%M')})"

    def save(self, *args, **kwargs):
        is_new = self._state.adding # Verifica se é uma nova instância
        super().save(*args, **kwargs) # Chama o método save original
        if is_new:
            logger.info("Nova Venda #%s salva no banco de dados. Total: %s, Pagamento: %s", self.id, self.total_amount, self.payment_method)
        else:
            logger.info("Venda #%s atualizada no banco de dados.", self.id) # Removido total_amount para consistência com o log de criação

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
    quantity = models.PositiveIntegerField(
        _("Quantidade"),
        help_text=_("Quantidade vendida deste produto.")
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
        # Calcula o subtotal automaticamente antes de salvar, se não for fornecido
        logger.debug("Preparando para salvar SaleItem. Produto: %s, Quantidade: %s", self.product.name if self.product else 'N/A', self.quantity)
        if not self.subtotal:
            self.subtotal = self.quantity * self.unit_price
            logger.debug("Subtotal do SaleItem calculado: %s", self.subtotal)

        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            logger.info("Novo SaleItem para Venda #%s salvo no banco. Produto: %s, Subtotal: %s", self.sale.id, self.product.name, self.subtotal)
        else:
            logger.info("SaleItem para Venda #%s atualizado no banco.", self.sale.id)
