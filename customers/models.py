from django.db import models
from django.utils.translation import gettext_lazy as _

class Customer(models.Model):
    name = models.CharField(
        _("Nome do Cliente"),
        max_length=255,
        help_text=_("Nome completo do cliente.")
    )
    phone_number = models.CharField(
        _("Telefone"),
        max_length=20,
        blank=True,
        help_text=_("Número de telefone do cliente (opcional).")
    )
    email = models.EmailField(
        _("E-mail"),
        blank=True,
        help_text=_("Endereço de e-mail do cliente (opcional).")
    )
    created_at = models.DateTimeField(
        _("Data de Cadastro"),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _("Cliente")
        verbose_name_plural = _("Clientes")
        ordering = ['name']

    def __str__(self):
        return self.name