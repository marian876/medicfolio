from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from .models import Analysis, Doctor, Appointment, Prescription, Consultation
from medication.models import ActiveProduct
from .forms import AnalysisFilterForm, ConsultationForm, DoctorForm, AppointmentForm, DoctorSearchForm, PrescriptionForm, AnalysisForm
from django.contrib import messages
from django.db.models import Q
from .filters import AnalysisFilter, AppointmentFilter, ConsultationFilter,PrescriptionFilter


class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctor/list.html'
    context_object_name = 'doctores'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', None)
        if search_query:
            queryset = queryset.filter(nombre__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = DoctorSearchForm(self.request.GET)
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

class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment/list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AppointmentFilter(self.request.GET, queryset=queryset)
        filtered_qs = self.filterset.qs

        search_query = self.request.GET.get('search')
        if search_query:
            filtered_qs = filtered_qs.filter(
                Q(doctor__nombre__icontains=search_query) |
                Q(motivo__icontains=search_query) |
                Q(acompanante__icontains=search_query) |
                Q(nota__icontains=search_query) | # Se agregó este campo
                Q(tipo__icontains=search_query)   # Se agregó este campo
            )
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
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

class ConsultationListView(ListView):
    model = Consultation
    template_name = 'consultation/list.html'
    context_object_name = 'consultations'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ConsultationFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
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

class PrescriptionListView(ListView):
    model = Prescription
    template_name = 'prescription/list.html'
    context_object_name = 'prescriptions'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PrescriptionFilter(self.request.GET, queryset=queryset)
        queryset = self.filterset.qs  # Aplica los filtros primero

        search_query = self.request.GET.get('search')
        if search_query:
            # Actualiza el queryset con el filtro de búsqueda
            queryset = queryset.filter(
                Q(consulta__cita__doctor__nombre__icontains=search_query) |
                Q(consulta__cita__motivo__icontains=search_query) |
                Q(consulta__diagnostico__icontains=search_query) |
                Q(producto__nombre_local__icontains=search_query) |
                Q(dosis__icontains=search_query) |
                Q(frecuencia__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

def prescription_create_view(request):
    if request.method == 'POST':
        print(request.POST)
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
        print(form.errors)
        form = PrescriptionForm()
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

class AnalysisListView(ListView):
    model = Analysis
    template_name = 'analysis/list.html'
    context_object_name = 'analyses'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AnalysisFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['filter_form'] = AnalysisFilterForm(self.request.GET)
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