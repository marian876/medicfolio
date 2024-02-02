from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from .models import Analysis, Doctor, Appointment, Prescription, Consultation
from users.models import RequestPatient
from medication.models import ActiveProduct
from .forms import ConsultationForm, DoctorForm, AppointmentForm, PrescriptionForm, AnalysisForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def get_patient_for_user(usuario):
    # ...
    if usuario.groups.filter(name='Familiar').exists():
        solicitud = RequestPatient.objects.filter(
            solicitante=usuario, 
            estado=RequestPatient.ESTADO_ACEPTADO
        ).first()
        return solicitud.paciente if solicitud else None

    if usuario.groups.filter(name='Cuidador').exists():
        solicitud = RequestPatient.objects.filter(
            solicitante=usuario, 
            estado=RequestPatient.ESTADO_ACEPTADO
        ).first()
        return solicitud.paciente if solicitud else None

@method_decorator(login_required, name='dispatch')
class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctor/list.html'
    context_object_name = 'doctores'

    def get_queryset(self):
        usuario = self.request.user
        queryset = super().get_queryset()
        paciente_id = self.request.GET.get('paciente')

        if paciente_id:
            queryset = queryset.filter(paciente__id=paciente_id)
        elif usuario.groups.filter(name='Paciente').exists():
            queryset = queryset.filter(paciente=usuario)
        elif usuario.groups.filter(name__in=['Familiar', 'Cuidador']).exists():
            paciente_asociado = get_patient_for_user(usuario)
            if paciente_asociado:
                queryset = queryset.filter(paciente=paciente_asociado)
            else:
                queryset = Doctor.objects.none()
        else:
            queryset = Doctor.objects.none()

        return queryset
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        pacientes = []

        # Agregar el propio usuario si es un paciente
        if usuario.groups.filter(name='Paciente').exists():
            pacientes.append(usuario)

        # Agregar pacientes asociados si el usuario es un familiar o cuidador
        if usuario.groups.filter(name__in=['Familiar', 'Cuidador']).exists():
            solicitudes_aceptadas = RequestPatient.objects.filter(
                solicitante=usuario,
                estado=RequestPatient.ESTADO_ACEPTADO
            )
            for solicitud in solicitudes_aceptadas:
                pacientes.append(solicitud.paciente)

        context['pacientes'] = pacientes
        return context

def doctor_create_view(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, 'Doctor agregado con éxito.')
            return redirect('consultations:doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'doctor/create.html', {'form': form})

def doctor_update_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor actualizado con éxito.')
            return redirect('consultations:doctor_list')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctor/update.html', {'form': form, 'doctor': doctor})

def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('consultations:doctor_list')
    return render(request, 'doctor/delete.html', {'doctor': doctor})

def doctor_detail_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctor/detail.html', {'doctor': doctor})

@method_decorator(login_required, name='dispatch')
class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment/list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        usuario = self.request.user
        queryset = super().get_queryset()
        pacientes_aceptados_ids = RequestPatient.objects.filter(
            Q(solicitante=usuario) | Q(paciente=usuario),
            estado=RequestPatient.ESTADO_ACEPTADO
        ).values_list('paciente_id', flat=True)

        # Si el usuario es un paciente, se añade su propio id
        if usuario.groups.filter(name='Paciente').exists():
            pacientes_aceptados_ids = list(pacientes_aceptados_ids) + [usuario.id]

        return queryset.filter(paciente_id__in=pacientes_aceptados_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        pacientes = []

        # Agregar el propio usuario si es un paciente
        if usuario.groups.filter(name='Paciente').exists():
            pacientes.append(usuario)

        # Agregar pacientes asociados si el usuario es un familiar o cuidador
        if usuario.groups.filter(name__in=['Familiar', 'Cuidador']).exists():
            solicitudes_aceptadas = RequestPatient.objects.filter(
                solicitante=usuario,
                estado=RequestPatient.ESTADO_ACEPTADO
            ).select_related('paciente')
            for solicitud in solicitudes_aceptadas:
                pacientes.append(solicitud.paciente)

        context['pacientes'] = pacientes
        return context

def appointment_create_view(request):
    form = AppointmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        appointment = form.save()
        messages.success(request, 'Cita creada con éxito.')
        return redirect('consultations:appointment_list')
    return render(request, 'appointment/create.html', {'form': form})

def appointment_detail_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    try:
        consultation = Consultation.objects.get(cita=appointment)
    except Consultation.DoesNotExist:
        consultation = None

    return render(request, 'appointment/detail.html', {
        'appointment': appointment,
        'consultation': consultation
    })

def appointment_update_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada con éxito.')
            return redirect('consultations:appointment_list')
        else:
            pass
    else:
        form = AppointmentForm(instance=appointment)
        if appointment.fecha_hora:
            form.fields['fecha_hora'].initial = appointment.fecha_hora.strftime('%Y-%m-%dT%H:%M')

    return render(request, 'appointment/update.html', {
        'form': form, 
        'appointment': appointment
    })

def appointment_delete_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Cita eliminada con éxito.')
        return redirect('consultations:appointment_list')
    return render(request, 'appointment/delete.html', {'appointment': appointment})

@method_decorator(login_required, name='dispatch')
class ConsultationListView(ListView):
    model = Consultation
    template_name = 'consultation/list.html'
    context_object_name = 'consultations'

    def get_queryset(self):
        usuario = self.request.user
        queryset = super().get_queryset()
        paciente_id = self.request.GET.get('paciente')

        if paciente_id:
            queryset = queryset.filter(paciente__id=paciente_id)
        else:
            pacientes_aceptados_ids = RequestPatient.objects.filter(
                Q(solicitante=usuario) | Q(paciente=usuario),
                estado=RequestPatient.ESTADO_ACEPTADO
            ).values_list('paciente_id', flat=True)

            # Si el usuario es un paciente, se añade su propio id
            if usuario.groups.filter(name='Paciente').exists():
                pacientes_aceptados_ids = list(pacientes_aceptados_ids) + [usuario.id]

            queryset = queryset.filter(paciente_id__in=pacientes_aceptados_ids)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        pacientes = []

        # Agregar el propio usuario si es un paciente
        if usuario.groups.filter(name='Paciente').exists():
            pacientes.append(usuario)

        # Agregar pacientes asociados si el usuario es un familiar o cuidador
        if usuario.groups.filter(name__in=['Familiar', 'Cuidador']).exists():
            solicitudes_aceptadas = RequestPatient.objects.filter(
                solicitante=usuario,
                estado=RequestPatient.ESTADO_ACEPTADO
            ).select_related('paciente')
            for solicitud in solicitudes_aceptadas:
                pacientes.append(solicitud.paciente)

        context['pacientes'] = pacientes
        return context
def consultation_create_view(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta creada con éxito.')
            return redirect('consultations:consultation_list')
    else:
        form = ConsultationForm()
    return render(request, 'consultation/create.html', {'form': form})

def consultation_update_view(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == 'POST':
        form = ConsultationForm(request.POST, request.FILES, instance=consultation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta actualizada con éxito.')
            return redirect('consultations:consultation_list')
    else:
        form = ConsultationForm(instance=consultation)
    return render(request, 'consultation/update.html', {'form': form, 'consultation': consultation})

def consultation_delete_view(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == 'POST':
        consultation.delete()
        messages.success(request, 'Consulta eliminada con éxito.')
        return redirect('consultations:consultation_list')
    return render(request, 'consultation/delete.html', {'consultation': consultation})

def consultation_detail_view(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    return render(request, 'consultation/detail.html', {'consultation': consultation})

@method_decorator(login_required, name='dispatch')
class PrescriptionListView(ListView):
    model = Prescription
    template_name = 'prescription/list.html'
    context_object_name = 'prescriptions'

    def get_queryset(self):
        usuario = self.request.user
        queryset = super().get_queryset()
        paciente_id = self.request.GET.get('paciente')

        if paciente_id:
            queryset = queryset.filter(paciente__id=paciente_id)
        else:
            pacientes_aceptados_ids = RequestPatient.objects.filter(
                Q(solicitante=usuario) | Q(paciente=usuario),
                estado=RequestPatient.ESTADO_ACEPTADO
            ).values_list('paciente_id', flat=True)

            # Si el usuario es un paciente, se añade su propio id
            if usuario.groups.filter(name='Paciente').exists():
                pacientes_aceptados_ids = list(pacientes_aceptados_ids) + [usuario.id]

            queryset = queryset.filter(paciente_id__in=pacientes_aceptados_ids)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        pacientes = []

        # Agregar el propio usuario si es un paciente
        if usuario.groups.filter(name='Paciente').exists():
            pacientes.append(usuario)

        # Agregar pacientes asociados si el usuario es un familiar o cuidador
        if usuario.groups.filter(name__in=['Familiar', 'Cuidador']).exists():
            solicitudes_aceptadas = RequestPatient.objects.filter(
                solicitante=usuario,
                estado=RequestPatient.ESTADO_ACEPTADO
            ).select_related('paciente')
            for solicitud in solicitudes_aceptadas:
                pacientes.append(solicitud.paciente)

        context['pacientes'] = pacientes
        return context


@login_required
def prescription_create_view(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            prescription = form.save()
            active_product, created = ActiveProduct.objects.update_or_create(
                producto=prescription.producto,  # Asegúrate de que 'producto' se refiere al campo correcto
                defaults={
                    'prescripcion': prescription,
                    'activo': prescription.activa  # Actualiza esto para reflejar el campo 'activa' de Prescription
                }
            )
            messages.success(request, 'Prescripción creada con éxito.')
            return redirect('consultations:prescription_list')
    else:
        form = PrescriptionForm()
    
    # Asegúrate de que la variable 'form' se pasa al contexto en ambos casos, POST y GET.
    return render(request, 'prescription/create.html', {'form': form})



def prescription_update_view(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, request.FILES, instance=prescription)
        if form.is_valid():
            form.save()
            messages.success(request, 'Prescripción actualizada con éxito.')
            return redirect('consultations:prescription_list')
    else:
        form = PrescriptionForm(instance=prescription)
    return render(request, 'prescription/update.html', {'form': form, 'prescription': prescription})

def prescription_delete_view(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == 'POST':
        prescription.delete()
        messages.success(request, 'Prescripción eliminada con éxito.')
        return redirect('consultations:prescription_list')
    return render(request, 'prescription/delete.html', {'prescription': prescription})

def prescription_detail_view(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    return render(request, 'prescription/detail.html', {'prescription': prescription})

@method_decorator(login_required, name='dispatch')
class AnalysisListView(ListView):
    model = Analysis
    template_name = 'analysis/list.html'
    context_object_name = 'analyses'

    def get_queryset(self):
        usuario = self.request.user
        queryset = super().get_queryset()
        paciente_id = self.request.GET.get('paciente')

        if paciente_id:
            queryset = queryset.filter(paciente__id=paciente_id)
        else:
            pacientes_aceptados_ids = RequestPatient.objects.filter(
                Q(solicitante=usuario) | Q(paciente=usuario),
                estado=RequestPatient.ESTADO_ACEPTADO
            ).values_list('paciente_id', flat=True)

            # Si el usuario es un paciente, se añade su propio id
            if usuario.groups.filter(name='Paciente').exists():
                pacientes_aceptados_ids = list(pacientes_aceptados_ids) + [usuario.id]

            queryset = queryset.filter(paciente_id__in=pacientes_aceptados_ids)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        pacientes = []

        # Agregar el propio usuario si es un paciente
        if usuario.groups.filter(name='Paciente').exists():
            pacientes.append(usuario)

        # Agregar pacientes asociados si el usuario es un familiar o cuidador
        if usuario.groups.filter(name__in=['Familiar', 'Cuidador']).exists():
            solicitudes_aceptadas = RequestPatient.objects.filter(
                solicitante=usuario,
                estado=RequestPatient.ESTADO_ACEPTADO
            ).select_related('paciente')
            for solicitud in solicitudes_aceptadas:
                pacientes.append(solicitud.paciente)

        context['pacientes'] = pacientes
        return context

def analysis_create_view(request):
    if request.method == 'POST':
        form = AnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Análisis creado con éxito.')
            return redirect('consultations:analysis_list')
    else:
        form = AnalysisForm()
    return render(request, 'analysis/create.html', {'form': form})

def analysis_update_view(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk)
    if request.method == 'POST':
        form = AnalysisForm(request.POST, request.FILES, instance=analysis)
        if form.is_valid():
            form.save()
            messages.success(request, 'Análisis actualizado con éxito.')
            return redirect('consultations:analysis_list')
    else:
        form = AnalysisForm(instance=analysis)
        # Asegúrate de que la fecha se establezca en el formato correcto para el widget de tipo 'date'.
        form.fields['fecha_analisis'].initial = analysis.fecha_analisis.strftime('%Y-%m-%d')
    return render(request, 'analysis/update.html', {'form': form, 'analysis': analysis})

def analysis_detail_view(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk)
    return render(request, 'analysis/detail.html', {'analysis': analysis})

def analysis_delete_view(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk)
    if request.method == 'POST':
        analysis.delete()
        messages.success(request, 'Análisis eliminado con éxito.')
        return redirect('consultations:analysis_list')
    return render(request, 'analysis/delete.html', {'analysis': analysis})