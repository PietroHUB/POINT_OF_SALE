from django.urls import path
from . import views

app_name = 'caixa'

urlpatterns = [
    # Rota raiz agora aponta para a tela de seleção de POS
    path('', views.select_pos_view, name='select_pos_page'),
    
    # A página de vendas agora espera um ID do ponto de venda
    path('pdv/<int:pos_id>/', views.sales_page_view, name='sales_page'),
]