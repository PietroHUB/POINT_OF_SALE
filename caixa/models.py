from django.db import models
from django.utils.translation import gettext_lazy as _

class PaymentMethod(models.Model):
    description = models.CharField(
        _("Descrição"),
        max_length=100,
        unique=True
    )
    requires_customer = models.BooleanField(
        _("Exige Cliente"),
        default=False,
        help_text=_("Marque esta opção se esta forma de pagamento exige a associação de um cliente à venda (ex: Fiado).")
    )
    # O campo ID (AutoField, Primary Key) é adicionado automaticamente pelo Django

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Forma de Pagamento"
        verbose_name_plural = "Formas de Pagamento"
        ordering = ['description'] # Opcional: ordena por descrição por padrão

class PointOfSale(models.Model):
    name = models.CharField(
        _("Nome do Ponto de Venda"),
        max_length=100,
        unique=True,
        help_text=_("Ex: Caixa 01, Terminal de Vendas, Balcão")
    )
    is_active = models.BooleanField(
        _("Ativo"),
        default=True,
        help_text=_("Desmarque para desativar este ponto de venda.")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Ponto de Venda")
        verbose_name_plural = _("Pontos de Venda")
        ordering = ['name']
