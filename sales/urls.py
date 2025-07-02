from django.urls import path
from . import views

app_name = 'sales' # Namespace para as URLs deste app

urlpatterns = [
    path('finalize/', views.finalize_sale, name='finalize_sale'),
    # Nova URL para o cupom
    path('receipt/<int:sale_id>/', views.sale_receipt_view, name='sale_receipt'),
]