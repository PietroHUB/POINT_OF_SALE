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
        unique=True,
        blank=True,       # Permitir que seja blank inicialmente, pois será gerado
        editable=False,   # Não editável diretamente em formulários, será gerado automaticamente
        help_text=_("Código interno/SKU único para o produto (gerado automaticamente).")
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

    def save(self, *args, **kwargs):
        # Verifica se é uma nova instância (primeiro save) e se o internal_code ainda não foi definido.
        if self._state.adding and not self.internal_code:
            # Primeiro, salva o objeto para que ele obtenha um PK (self.pk).
            # Esta chamada a super().save() irá inserir o registro no banco.
            super().save(*args, **kwargs)

            # Agora que o objeto tem um PK, podemos usá-lo para gerar um código interno único.
            # Formato ajustado para apenas números, com padding de 6 dígitos.
            generated_code = f"{self.pk:06d}"
            self.internal_code = generated_code

            # Atualiza o registro no banco de dados apenas com o novo internal_code,
            # sem disparar o método save() completo novamente (evita recursão e sinais desnecessários).
            Product.objects.filter(pk=self.pk).update(internal_code=self.internal_code)
        else:
            # Se for uma atualização de um produto existente, ou se o internal_code já estiver definido.
            super().save(*args, **kwargs)
