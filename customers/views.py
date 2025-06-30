from django.http import JsonResponse
from .models import Customer
from django.contrib.auth.decorators import login_required

#@login_required
def search_customers(request):
    query = request.GET.get('q', '')
    customers = []
    if query:
        # Busca clientes cujo nome contém a query (insensível a maiúsculas/minúsculas)
        customers = Customer.objects.filter(name__icontains=query)[:10] # Limita a 10 resultados
    
    data = [
        {'id': customer.id, 'name': customer.name}
        for customer in customers
    ]
    
    return JsonResponse(data, safe=False)