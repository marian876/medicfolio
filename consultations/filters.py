# filters.py
import django_filters
from products.models import Presentation
from .models import Analysis, Appointment, Consultation, Prescription
from django.db.models import Q


class AppointmentFilter(django_filters.FilterSet):
    CHOICES = (
        ('True', 'Sí'),
        ('False', 'No'),
    )
    pendiente = django_filters.ChoiceFilter(choices=CHOICES, method='filter_pendiente', label='Pendiente')

    class Meta:
        model = Appointment
        fields = []

    def filter_pendiente(self, queryset, name, value):
        if value == 'True':
            return queryset.filter(pendiente=True)
        elif value == 'False':
            return queryset.filter(pendiente=False)
        return queryset

class PrescriptionFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter', label='Buscar')
    CHOICES = (
        ('True', 'Sí'),
        ('False', 'No'),
    )
    activa = django_filters.ChoiceFilter(choices=CHOICES, method='filter_activa', label='Activa')

    class Meta:
        model = Prescription
        fields = []

    def filter_activa(self, queryset, name, value):
        if value == 'True':
            return queryset.filter(activa=True)
        elif value == 'False':
            return queryset.filter(activa=False)
        return queryset

    def search_filter(self, queryset, name, value):
        # Asegúrate de que esta consulta cubra todos los campos en los que deseas buscar
        return queryset.filter(
            Q(consulta__cita__doctor__nombre__icontains=value) |
            Q(consulta__cita__motivo__icontains=value) |
            Q(consulta__diagnostico__icontains=value) |
            Q(producto__nombre_local__icontains=value) |
            Q(dosis__icontains=value) |
            Q(frecuencia__icontains=value)
        )

class ConsultationFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='multi_field_search', label='Buscar')

    class Meta:
        model = Consultation
        fields = []

    def multi_field_search(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(cita__doctor__nombre__icontains=value) |
                Q(diagnostico__icontains=value) |
                Q(notas__icontains=value)
            )
        return queryset
    
class AnalysisFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter', label='Buscar')
    realizado = django_filters.ChoiceFilter(choices=[('True', 'Sí'), ('False', 'No')], method='filter_realizado', label='Realizado')

    class Meta:
        model = Analysis
        fields = []

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(consulta__cita__doctor__nombre__icontains=value) |
            Q(fecha_analisis__icontains=value) |
            Q(descripcion__icontains=value) 
        )
    
    def filter_realizado(self, queryset, name, value):
        if value == 'True':
            return queryset.filter(realizado=True)
        elif value == 'False':
            return queryset.filter(realizado=False)
        return queryset
