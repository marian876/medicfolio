from django.contrib import admin
from .models import CalendarEvent

class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'hora_inicio', 'hora_fin', 'paciente', 'cita', 'consulta', 'creado_por')
    list_filter = ('hora_inicio', 'hora_fin', 'paciente')
    search_fields = ('titulo', 'descripcion', 'paciente__username', 'cita__motivo', 'consulta__diagnostico')
    raw_id_fields = ('paciente', 'cita', 'consulta', 'creado_por')

admin.site.register(CalendarEvent, CalendarEventAdmin)
