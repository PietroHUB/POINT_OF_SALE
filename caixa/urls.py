from django.urls import path
from . import views

app_name = 'caixa' # Namespace para as URLs deste app

urlpatterns = [
    path('', views.sales_page_view, name='sales_page'),
]