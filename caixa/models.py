from django.db import models

class PaymentMethod(models.Model):
    description = models.CharField(max_length=100, unique=True, verbose_name="Descrição")
    # O campo ID (AutoField, Primary Key) é adicionado automaticamente pelo Django

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Forma de Pagamento"
        verbose_name_plural = "Formas de Pagamento"
        ordering = ['description'] # Opcional: ordena por descrição por padrão
