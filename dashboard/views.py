from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from consultations.models import Prescription, Appointment
from users.models import RequestPatient
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef
from consultations.models import Prescription, Appointment
from products.models import Product

def get_patients_for_user(usuario):
    pacientes = []
    if usuario.groups.filter(name='Familiar').exists() or usuario.groups.filter(name='Cuidador').exists():
        solicitudes = RequestPatient.objects.filter(
            Q(solicitante=usuario) | Q(paciente=usuario),
            estado=RequestPatient.ESTADO_ACEPTADO
        )
        for solicitud in solicitudes:
            pacientes.append(solicitud.paciente)
    elif usuario.groups.filter(name='Paciente').exists():
        pacientes.append(usuario)
    return pacientes

@login_required
def dashboard_view(request):
    usuario = request.user
    paciente_id = request.GET.get('paciente')
    
    pacientes_relacionados = get_patients_for_user(usuario)
    pacientes_aceptados_ids = [paciente.id for paciente in pacientes_relacionados]
    
    # Subconsulta para obtener la última prescripción para cada producto
    ultima_prescripcion_subquery = Prescription.objects.filter(
        producto_id=OuterRef('pk'),
        paciente_id=OuterRef('paciente_id')
    ).order_by('-creado_el').values('creado_el')[:1]
    
    if paciente_id:
        paciente_id = int(paciente_id)  # Convertir a entero si es necesario
        appointments = Appointment.objects.filter(paciente_id=paciente_id, pendiente=True).order_by('creado_el')
        # Filtrar las prescripciones activas y obtener la última para cada producto
        prescription_products = Prescription.objects.filter(
            paciente_id=paciente_id,
            activa=True
        ).annotate(
            ultima_prescripcion=Subquery(ultima_prescripcion_subquery)
        ).order_by('-ultima_prescripcion')
    else:
        appointments = Appointment.objects.filter(paciente_id__in=pacientes_aceptados_ids, pendiente=True).order_by('creado_el')
        prescription_products = Prescription.objects.filter(
            paciente_id__in=pacientes_aceptados_ids,
            activa=True
        ).annotate(
            ultima_prescripcion=Subquery(ultima_prescripcion_subquery)
        ).order_by('-ultima_prescripcion')
    
    # Lista de productos a comprar
    products_to_purchase = [
        prescripcion.producto for prescripcion in prescription_products
        if prescripcion.producto.dias_de_cobertura <= 7 or prescripcion.producto.dias_de_cobertura == 99999
    ]

    
    context = {
        'appointments': appointments,
        'prescription_products': prescription_products,
        'products_to_purchase': products_to_purchase,
        'pacientes_activos': pacientes_relacionados,
    }
    
    return render(request, 'dashboard/dashboard.html', context)