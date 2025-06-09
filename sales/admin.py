from django.contrib import admin
from .models import Sale, SaleItem

class SaleItemInline(admin.TabularInline): # Ou admin.StackedInline para um layout diferente
    model = SaleItem
    extra = 0 # Não mostrar campos extras para adicionar SaleItem por padrão
    readonly_fields = ('product', 'quantity', 'unit_price', 'subtotal') # Torna os campos somente leitura no inline
    can_delete = False # Impede a exclusão de itens de venda a partir do admin da Venda

    def has_add_permission(self, request, obj=None):
        return False # Impede a adição de novos itens de venda a partir do admin da Venda

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_amount', 'payment_method', 'created_at') # Campos a serem exibidos na lista de vendas
    list_filter = ('payment_method', 'created_at') # Filtros
    search_fields = ('id', 'payment_method') # Campos de busca
    readonly_fields = ('total_amount', 'payment_method', 'created_at') # Torna campos somente leitura no formulário de edição da Venda
    inlines = [SaleItemInline] # Permite ver os SaleItems dentro da página de detalhes da Sale

    def has_add_permission(self, request):
        return False # Impede a criação de novas vendas diretamente pelo admin

    def has_change_permission(self, request, obj=None):
        return False # Impede a edição de vendas existentes pelo admin (exceto pelos inlines)

    def has_delete_permission(self, request, obj=None):
        return False # Impede a exclusão de vendas pelo admin

# Opcional: Registrar SaleItem separadamente se quiser uma visão direta deles,
# mas geralmente é melhor visualizá-los através da Sale.
# @admin.register(SaleItem)
# class SaleItemAdmin(admin.ModelAdmin):
#     list_display = ('sale', 'product', 'quantity', 'unit_price', 'subtotal')
#     list_filter = ('product',)
#     search_fields = ('sale__id', 'product__name')
