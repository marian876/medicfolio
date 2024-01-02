from django.contrib import admin

from .models import Dispenser

#admin.site.register(Dispenser)

from django.contrib import admin
from .models import Dispenser, DispenserProducts

class DispenserProductsInline(admin.TabularInline):
    model = DispenserProducts
    extra = 1  # Número de formularios adicionales para mostrar

class DispenserAdmin(admin.ModelAdmin):
    inlines = [DispenserProductsInline,]

admin.site.register(Dispenser, DispenserAdmin)
