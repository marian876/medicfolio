from django.shortcuts import render
from consultations.models import Appointment
from products.models import Product

def index(request):
    appointments_active = Appointment.objects.filter(pendiente=True).order_by('fecha_hora')
    prescription_products = Product.objects.filter(prescriptions__activa=True).distinct()

    days_to_consider = int(request.GET.get('days', 7))
    all_products = Product.objects.all()

    products_purchase = [product for product in all_products if product.dias_de_cobertura <= days_to_consider]

    context = {
        'appointments_active': appointments_active,
        'prescription_products': prescription_products,
        'products_purchase': products_purchase,
    }

    return render(request, 'index.html', context)

