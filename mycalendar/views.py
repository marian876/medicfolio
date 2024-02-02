from datetime import datetime, timedelta
from django.shortcuts import render
from consultations.models import Appointment, Consultation, Prescription
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from users.models import RequestPatient

def get_patient_for_user(usuario):
    pacientes_ids = []
    if usuario.groups.filter(name='Paciente').exists():
        pacientes_ids.append(usuario.id)
    elif usuario.groups.filter(name='Familiar').exists() or usuario.groups.filter(name='Cuidador').exists():
        solicitudes = RequestPatient.objects.filter(solicitante=usuario, estado=RequestPatient.ESTADO_ACEPTADO)
        pacientes_ids.extend(solicitud.paciente.id for solicitud in solicitudes)
    return pacientes_ids

@login_required
def view_calendar(request):
    usuario = request.user
    paciente_id = request.GET.get('paciente')
    pacientes_ids = get_patient_for_user(usuario)

    appointments_query = Appointment.objects.filter(paciente_id__in=pacientes_ids, pendiente=True)
    consultations_query = Consultation.objects.filter(paciente_id__in=pacientes_ids)
    prescriptions_query = Prescription.objects.filter(paciente_id__in=pacientes_ids, activa=True)

    if paciente_id:
        appointments_query = appointments_query.filter(paciente_id=paciente_id)
        consultations_query = consultations_query.filter(paciente_id=paciente_id)
        prescriptions_query = prescriptions_query.filter(paciente_id=paciente_id)

    events = [
        {
            "title": f"Cita: {appointment.doctor.nombre} - {appointment.motivo}",
            "start": appointment.fecha_hora.isoformat(),
            "end": (appointment.fecha_hora + timedelta(hours=1)).isoformat(),
            "url": reverse('consultations:appointment_detail', args=[appointment.pk]),
            "color": "#3788d8",
        } for appointment in appointments_query
    ] + [
        {
            "title": f"Consulta: {consultation.cita.doctor.nombre} - {consultation.diagnostico}",
            "start": consultation.cita.fecha_hora.isoformat(),
            "end": (consultation.cita.fecha_hora + timedelta(hours=1)).isoformat(),
            "url": reverse('consultations:consultation_detail', args=[consultation.pk]),
            "color": "#28a745",
        } for consultation in consultations_query
    ] + [
        {
            "title": f"Reabastecer {prescription.producto.nombre_local}",
            "start": (datetime.now() + timedelta(days=prescription.producto.dias_de_cobertura)).date().isoformat(),
            "color": "darkred" if prescription.producto.dias_de_cobertura <= 0 else "red",
            "textColor": "white",
            "allDay": True,
        } for prescription in prescriptions_query if prescription.producto.dias_de_cobertura <= 7
    ]

    return JsonResponse(events, safe=False)
