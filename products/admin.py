from django.contrib import admin
from .models import Product
"""
    Explicação das alterações:

    1) from .models import Product: Importamos o modelo Product que você criou no models.py.
    
    2) @admin.register(Product): 
        Este é um decorador que registra o modelo Product com a classe de administração ProductAdmin 
        que definimos logo abaixo. 
        É uma forma mais "pythônica" de fazer admin.site.register(Product, ProductAdmin).
    
    3) class ProductAdmin(admin.ModelAdmin):
        Criamos uma classe que herda de admin.ModelAdmin. 
        Isso nos permite personalizar como o modelo Product é exibido e gerenciado na interface 
        de administração.

        list_display: 
        Define quais campos do modelo Product serão exibidos na lista de produtos na página de administração.

        search_fields: 
        Adiciona uma barra de pesquisa que permitirá buscar produtos pelos campos especificados 
        (nome, código interno, código de barras, descrição).

        list_filter: 
        Adiciona filtros na barra lateral para facilitar a navegação pelos produtos 
        (por data de criação e atualização, por exemplo).
        
        ordering: 
        Define a ordenação padrão na lista de produtos.
        
        readonly_fields (comentado): 
        Se você descomentar esta linha, os campos created_at e updated_at não poderão ser editados 
        diretamente no formulário de administração (o que faz sentido, já que eles são auto_now_add e auto_now).


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'internal_code',
        'barcode',
        'price',
        'purchase_price',
        'stock_quantity',
        'created_at',
        'updated_at'
    )
    search_fields = ('name', 'internal_code', 'barcode', 'description')
    list_filter = ('created_at', 'updated_at')
    ordering = ('name',)
    # readonly_fields = ('created_at', 'updated_at') # Se quiser que não sejam editáveis no form
"""

admin.site.register(Product)
