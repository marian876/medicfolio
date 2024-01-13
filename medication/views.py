# medication/views.py

from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from .models import Product, Prescription
from .filters import MedicationFilter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

class ActiveProductListView(ListView):
    model = Product
    template_name = 'medication/list.html'
    filterset_class = MedicationFilter

    def get_queryset(self):
        # Filtra para obtener solo los productos con al menos una prescripción activa
        queryset = super().get_queryset().filter(prescriptions__activa=True).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        days_to_consult = int(self.request.GET.get('days', 1))

        products_with_insufficient_stock = []
        for product in context['object_list']:
            active_prescription = product.prescriptions.filter(activa=True).first()
            if active_prescription:
                total_doses_needed = active_prescription.dosis * days_to_consult
                if product.existencia < total_doses_needed:
                    products_with_insufficient_stock.append({
                        'product': product,
                        'existencia': product.existencia,
                        'faltan': total_doses_needed - product.existencia
                    })

        context['insufficient_stock_products'] = products_with_insufficient_stock
        context['days'] = days_to_consult
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



