# medication/views.py

from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView

from users.models import RequestPatient
from .models import Product, Prescription
from .filters import MedicationFilter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.db.models import Q
from django.conf import settings
from django.apps import apps

UserModel = apps.get_model(settings.AUTH_USER_MODEL)

class ActiveProductListView(ListView):
    model = Product
    template_name = 'medication/list.html'
    filterset_class = MedicationFilter

    def get_queryset(self):
        usuario = self.request.user
        queryset = super().get_queryset().filter(prescriptions__activa=True).distinct()

        # Aquí se filtra por paciente si se proporciona
        paciente_id = self.request.GET.get('paciente')
        if paciente_id:
            queryset = queryset.filter(paciente_id=paciente_id)
        else:
            pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir la lista de pacientes al contexto
        context['pacientes'] = UserModel.objects.filter(
            id__in=RequestPatient.objects.filter(
                Q(solicitante=self.request.user) | Q(paciente=self.request.user),
                estado=RequestPatient.ESTADO_ACEPTADO
            ).values_list('paciente_id', flat=True)
        )
        return context


def export_products_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="stock_insuficiente.pdf"'

    # Crea el objeto canvas para el PDF
    p = canvas.Canvas(response)

    # Obtiene el número de días del formulario o usa un valor por defecto
    days_to_consult = int(request.GET.get('days', 1))

    # Título del PDF
    p.setFont("Helvetica-Bold", 12)  # Fuente en negrita
    p.drawString(100, 800, f"Reporte de Productos con Stock Insuficiente para {days_to_consult} días")
    p.setFont("Helvetica", 10)  # Cambia la fuente a normal para el contenido

    # Inicializa la posición en el eje Y para la lista de productos
    y_position = 780
    product_counter = 1  # Contador para la lista numerada

    # Itera sobre los productos y verifica el stock insuficiente
    for product in Product.objects.filter(prescriptions__activa=True).distinct():
        active_prescription = get_object_or_404(Prescription, producto=product, activa=True)
        total_doses_needed = active_prescription.dosis * days_to_consult

        if product.existencia < total_doses_needed:
            faltan = total_doses_needed - product.existencia
            p.drawString(100, y_position, f"{product_counter}. {product.nombre_local} - Existencia: {product.existencia} - Faltan: {faltan}")
            y_position -= 20  # Mueve hacia abajo para el próximo producto
            product_counter += 1  # Incrementa el contador de productos

    # Finaliza la página y guarda el PDF
    p.showPage()
    p.save()

    return response