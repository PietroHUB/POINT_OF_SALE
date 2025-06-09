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
    list_display = ('id', 'total_amount', 'created_at', 'display_payment_methods') # Campos a serem exibidos na lista de vendas
    list_filter = ('created_at',) # Filtros
    search_fields = ('id',) # Campos de busca
    readonly_fields = ('total_amount', 'created_at', 'display_payment_methods') # Torna campos somente leitura
    inlines = [SaleItemInline] # Permite ver os SaleItems dentro da página de detalhes da Sale

    def has_add_permission(self, request):
        return False # Impede a criação de novas vendas diretamente pelo admin

    def has_change_permission(self, request, obj=None):
        return False # Impede a edição de vendas existentes pelo admin (exceto pelos inlines)

    def has_delete_permission(self, request, obj=None):
        return False # Impede a exclusão de vendas pelo admin

    def display_payment_methods(self, obj):
        # obj é uma instância de Sale
        # obj.payments.all() usa o related_name='payments' do ForeignKey em SalePayment
        payments = obj.payments.all()
        return ", ".join([f"{p.payment_method.description} (R$ {p.amount})" for p in payments]) if payments else "N/A"
    display_payment_methods.short_description = "Formas de Pagamento"

# Opcional: Registrar SaleItem separadamente se quiser uma visão direta deles,
# mas geralmente é melhor visualizá-los através da Sale.
# @admin.register(SaleItem)
# class SaleItemAdmin(admin.ModelAdmin):
#     list_display = ('sale', 'product', 'quantity', 'unit_price', 'subtotal')
#     list_filter = ('product',)
#     search_fields = ('sale__id', 'product__name')
