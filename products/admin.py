from django.contrib import admin
from django.utils.formats import date_format

from .models import Product, Presentation, Specialty

class ProductAdmin(admin.ModelAdmin):
    fields = (
        'nombre_local',
        'venta_controlada',
        'fabricante',
        'presentacion',
        'cantidad_caja',
        'precio',
        'existencia',
        'compuesto_principal',
        'descripcion',
        'especialidad',
        'usos',
        'posologia',
        'embarazo',
        'lactancia',
        'contraindicaciones',
        'precauciones',
        'reacciones_adversas',
        'interacciones',
        'codigo_barras',
        'pais',
        'imagen_caja',
    )
    list_display = ('__str__', 'slug')

    def formatted_created_at(self, obj):
        return date_format(obj.creado_el, "SHORT_DATE_FORMAT")
    formatted_created_at.short_description = 'Fecha de Creación'

class PresentacionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Presentation, PresentacionAdmin)
admin.site.register(Specialty, EspecialidadAdmin)