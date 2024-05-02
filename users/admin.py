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

# Cambios aquí: Ahora heredando de BaseUserAdmin
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm  # Usamos el formulario por defecto que incluye el cambio de contraseña
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')  # Agregamos 'is_staff' para más información
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

class RequestPatientAdmin(admin.ModelAdmin):
    list_display = ('solicitante', 'paciente', 'estado')
    search_fields = ('solicitante__username', 'paciente__username')
    list_filter = ('estado',)



admin.site.register(User, UserAdmin)
admin.site.register(PatientProfile, ProfileAdmin)
admin.site.register(RequestPatient, RequestPatientAdmin)
