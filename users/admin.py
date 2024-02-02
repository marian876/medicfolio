from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import User, PatientProfile, RequestPatient

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','celular', 'fecha_nacimiento', 'encargado', 'alergias', 'enfermedades_base', 'cirugias', 'enfermedades_familiares', 'historial','foto')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user__is_active', 'user__is_staff')
    fieldsets = (
        (None, {'fields': ('user','celular', 'historial', 'fecha_nacimiento', 'encargado', 'alergias', 'enfermedades_base', 'cirugias', 'enfermedades_familiares','foto')}),
    )

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')  # Ajusta los campos que quieras mostrar
    search_fields = ('username', 'email')

class RequestPatientAdmin(admin.ModelAdmin):
    list_display = ('solicitante', 'paciente', 'estado')
    search_fields = ('solicitante__username', 'paciente__username')
    list_filter = ('estado',)


admin.site.register(User, UserAdmin)
admin.site.register(PatientProfile, ProfileAdmin)
admin.site.register(RequestPatient, RequestPatientAdmin)
