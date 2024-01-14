from django.views.generic import ListView
from django.shortcuts import render
from consultations.models import Appointment
from products.models import Product

# Esta vista basada en clase maneja la lista de citas pendientes
class DashboardAppointmentListView(ListView):
    model = Appointment
    template_name = 'dashboard/snippets/appointment.html'
    context_object_name = 'appointments_active'

    def get_queryset(self):
        return Appointment.objects.filter(pendiente=True).order_by('fecha_hora')

# Esta vista basada en clase maneja la lista de productos con prescripciones activas
class DashboardMedicationListView(ListView):
    model = Product
    template_name = 'dashboard/snippets/medication.html'
    context_object_name = 'prescription_products'

    def get_queryset(self):
        return Product.objects.filter(prescriptions__activa=True).distinct()

# Esta función de vista combina la información de citas y productos para el dashboard
def dashboard_view(request):
    appointments_active = DashboardAppointmentListView().get_queryset()
    prescription_products = DashboardMedicationListView().get_queryset()

    context = {
        'appointments_active': appointments_active,
        'prescription_products': prescription_products,
    }

    return render(request, 'dashboard.html', context)

class DashboardPurchaseListView(ListView):
    model = Product
    template_name = 'dashboard/snippets/purchase.html'
    context_object_name = 'products_purchase'

    def get_queryset(self):
        days_to_consider = self.request.GET.get('days', 7)  
        return Product.objects.filter(dias_de_cobertura__lte=days_to_consider)