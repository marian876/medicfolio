from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import User, Profile

# Clase para personalizar la visualización del modelo User en el admin
class UserAdmin(BaseUserAdmin):
    pass
# Clase para personalizar la visualización del modelo Profile en el admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fecha_nacimiento', 'encargado', 'alergias', 'enfermedades_base', 'cirugias', 'enfermedades_familiares', 'historial')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user__is_active', 'user__is_staff')
    fieldsets = (
        (None, {'fields': ('user', 'historial', 'fecha_nacimiento', 'encargado', 'alergias', 'enfermedades_base', 'cirugias', 'enfermedades_familiares')}),
    )

# Registrar los modelos con sus clases de administración personalizadas
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
