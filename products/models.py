from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    name = models.CharField(
        _("Nome do Produto"),
        max_length=255,
        help_text=_("Nome completo do produto.")
    )
    description = models.TextField(
        _("Descrição"),
        blank=True,
        null=True,
        help_text=_("Descrição detalhada do produto (opcional).")
    )
    price = models.DecimalField(
        _("Preço de Venda"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Preço unitário de venda do produto.")
    )
    purchase_price = models.DecimalField(
        _("Preço de Compra"),
        max_digits=10,
        decimal_places=2,
        null=True, # Pode ser que você não tenha o preço de compra imediatamente
        blank=True,
        help_text=_("Preço unitário de compra do produto (opcional).")
    )
    internal_code = models.CharField(
        _("Código Interno"),
        max_length=50,
        unique=True, # Geralmente um código interno/SKU é único
        help_text=_("Código interno/SKU único para o produto.")
    )
    stock_quantity = models.PositiveIntegerField(
        _("Quantidade em Estoque"),
        default=0,
        help_text=_("Quantidade atual do produto em estoque.")
    )
    barcode = models.CharField(
        _("Código de Barras"),
        max_length=100,
        blank=True,
        null=True,
        unique=True, # Geralmente códigos de barra são únicos
        help_text=_("Código de barras do produto (opcional, mas recomendado).")
    )
    created_at = models.DateTimeField(
        _("Data de Criação"),
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        _("Data de Atualização"),
        auto_now=True,
        editable=False
    )

    class Meta:
        verbose_name = _("Produto")
        verbose_name_plural = _("Produtos")
        ordering = ['name'] # Ordenar por nome por padrão

    def __str__(self):
        return self.name
