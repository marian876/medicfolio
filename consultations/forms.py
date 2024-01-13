from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Analysis, Doctor, Appointment, Prescription, Consultation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column,Field, Div

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['nombre', 'especialidad', 'telefono_reserva',   
                  'ubicacion', 'telefono_personal',
                  'notas','imagen']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'tipo', 'doctor', 'fecha_hora', 'motivo', 'costo', 'acompanante', 
            'pendiente', 'cita_posterior', 'nota'
        ]
        widgets = {
            'pendiente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),  # Asegúrate de incluir este widget
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'fecha_hora': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'costo': forms.NumberInput(attrs={'class': 'form-control'}),
            'acompanante': forms.TextInput(attrs={'class': 'form-control'}),
            'cita_posterior': forms.NumberInput(attrs={'class': 'form-control'}),
            'nota': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('doctor', css_class='form-group col-md-6 mb-0'),
                Column('fecha_hora', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('motivo', css_class='form-group col-md-6 mb-0'),
                Column('costo', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('acompanante', css_class='form-group col-md-6 mb-0'),
            ),
            'pendiente',
            Row(
                Column('notas', css_class='form-group col-12 mb-0'),
            ),
        )
        if self.instance and self.instance.fecha_hora:
            self.initial['fecha_hora'] = self.instance.fecha_hora.strftime('%Y-%m-%dT%H:%M')

class AppointmentFilterForm(forms.Form):
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        required=False,
        label=_("Doctor")
    )
    acompanante = forms.CharField(max_length=255, required=False, label=_("Acompañante"))
    pendiente = forms.BooleanField(
        required=False, 
        label=_("Pendiente"),
        initial=True
    )

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['cita', 'audio', 'diagnostico', 'pdf_indicaciones', 'notas']
        widgets = {
            'cita': forms.Select(attrs={'class': 'form-control'}),
            'audio': forms.FileInput(attrs={'class': 'form-control-file'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pdf_indicaciones': forms.FileInput(attrs={'class': 'form-control-file'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(ConsultationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'cita',
            'audio',
            'diagnostico',
            'pdf_indicaciones',
            'notas',
        )

class DoctorSearchForm(forms.Form):
    search = forms.CharField(required=False, label='Buscar')

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['consulta', 'producto', 'dosis', 'frecuencia', 'periodo', 'periodo_indefinido','activa']
        widgets = {
            'consulta': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control'}),
            'periodo': forms.NumberInput(attrs={'class': 'form-control'}),
            'periodo_indefinida': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activa ': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(PrescriptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'consulta',
            'producto',
            'dosis',
            'frecuencia',
            'periodo',
            Div(
                Field('activa', css_class='checkbox', style='margin-left: 0;'),
                css_class='form-group'
            ),
        )

class PrescriptionSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar prescripciones...'})
    )

class PrescriptionFilterForm(forms.Form):
    prescription = forms.ModelChoiceField(
    queryset=Prescription.objects.all(),
    required=False,
    label=_("Prescripción")
    )
    activa = forms.BooleanField(
    required=False, 
    label=_("Activa"),
    initial=True
    )

class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ['consulta', 'fecha_analisis', 'descripcion', 'realizado', 'resultado_pdf']
        widgets = {
            'realizado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'consulta': forms.Select(attrs={'class': 'form-control'}),
            'fecha_analisis': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'resultado_pdf': forms.FileInput(attrs={'class': 'form-control-file'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(AnalysisForm, self).__init__(*args, **kwargs)
        # Inicialización correcta de la fecha de análisis cuando se actualiza un análisis
        if 'instance' in kwargs:
            self.fields['fecha_analisis'].initial = kwargs['instance'].fecha_analisis.strftime('%Y-%m-%d')
        self.helper = FormHelper(self)

class AnalysisFilterForm(forms.Form):
    REALIZADO_CHOICES = (
        ('', 'Todos'),
        ('True', 'Sí'),
        ('False', 'No'),
    )
    realizado = forms.ChoiceField(choices=REALIZADO_CHOICES, required=False, label=_("Realizado"))

