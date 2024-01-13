import django_filters
from .models import Product, Specialty

class ProductFilter(django_filters.FilterSet):
    nombre_local = django_filters.CharFilter(lookup_expr='icontains')
    uso_cotidiano = django_filters.BooleanFilter()
    venta_controlada = django_filters.BooleanFilter()
    existencia = django_filters.NumberFilter()
    especialidad = django_filters.ModelChoiceFilter(queryset=Specialty.objects.all())

    class Meta:
        model = Product
        fields = ['nombre_local', 'uso_cotidiano', 'venta_controlada', 'existencia', 'especialidad']
