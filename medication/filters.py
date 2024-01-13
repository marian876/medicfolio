# medication/filters.py

import django_filters
from django.db.models import Q
from products.models import Product

class MedicationFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter', label='Buscar')
    prescriptions_activa = django_filters.BooleanFilter(method='filter_prescriptions_activa', label='Prescripción activa')

    class Meta:
        model = Product
        fields = []

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(nombre_local__icontains=value) |
            Q(descripcion__icontains=value)
        )

    def filter_prescriptions_activa(self, queryset, name, value):
        if value:
            return queryset.filter(prescriptions__activa=True).distinct()
        else:
            return queryset.filter(prescriptions__activa=False).distinct()

