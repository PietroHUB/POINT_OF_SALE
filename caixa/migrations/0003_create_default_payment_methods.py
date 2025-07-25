# Generated by Django 5.2.1 on 2025-06-30 14:04

from django.db import migrations

# Lista de formas de pagamento padrão a serem criadas.
DEFAULT_PAYMENT_METHODS = [
    {'description': 'Dinheiro', 'requires_customer': False},
    {'description': 'Pix', 'requires_customer': False},
    {'description': 'Cartão de Crédito', 'requires_customer': False},
    {'description': 'Cartão de Débito', 'requires_customer': False},
    {'description': 'Fiado', 'requires_customer': True},
]

def create_default_payment_methods(apps, schema_editor):
    """
    Cria as formas de pagamento padrão no banco de dados.
    """
    PaymentMethod = apps.get_model('caixa', 'PaymentMethod')
    for method_data in DEFAULT_PAYMENT_METHODS:
        # Usa get_or_create para evitar criar duplicatas se a migração for executada novamente.
        PaymentMethod.objects.get_or_create(
            description=method_data['description'],
            defaults={'requires_customer': method_data['requires_customer']}
        )

def remove_default_payment_methods(apps, schema_editor):
    """
    Remove as formas de pagamento padrão (opcional, para reverter a migração).
    """
    PaymentMethod = apps.get_model('caixa', 'PaymentMethod')
    descriptions_to_delete = [item['description'] for item in DEFAULT_PAYMENT_METHODS]
    PaymentMethod.objects.filter(description__in=descriptions_to_delete).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('caixa', '0002_paymentmethod_requires_customer'),
    ]

    operations = [
        migrations.RunPython(create_default_payment_methods, reverse_code=remove_default_payment_methods),
    ]
