from django.contrib import admin
from .models import Product

#admin.site.register(Product)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'internal_code', # Adicionando o código interno
        'price',         # Adicionando o preço de venda
        'stock_quantity',# Adicionando a quantidade em estoque
        'barcode',
        'created_at',
        'updated_at'
    )
    search_fields = ('name', 'internal_code', 'barcode', 'description')
    list_filter = ('created_at', 'updated_at')
    ordering = ('name',)