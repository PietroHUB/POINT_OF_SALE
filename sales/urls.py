from django.urls import path
from . import views

app_name = 'sales' # Namespace para as URLs deste app

urlpatterns = [
    path('finalize/', views.finalize_sale, name='finalize_sale'), # URL para finalizar a venda
]