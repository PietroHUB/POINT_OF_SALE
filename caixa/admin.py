from django.contrib import admin
from .models import PaymentMethod, PointOfSale

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('description', 'requires_customer')
    list_filter = ('requires_customer',)
    ordering = ('description',)

@admin.register(PointOfSale)
class PointOfSaleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('name',)
