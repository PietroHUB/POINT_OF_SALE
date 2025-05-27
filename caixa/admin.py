from django.contrib import admin
from products.models import Product # Importar Product do app 'products'
from .models import PaymentMethod # PaymentMethod é local deste app 'caixa'

# Se você precisar registrar Product no admin A PARTIR do app caixa,
# o que não é comum (geralmente cada app registra seus próprios modelos),
# você faria isso aqui. Mas o Product já está registrado em products/admin.py.
# Se você não precisa de uma configuração de admin diferente para Product aqui,
# não precisa importá-lo ou registrá-lo novamente.

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    search_fields = ('description',)
    ordering = ('id',) # Ou 'description' se preferir
