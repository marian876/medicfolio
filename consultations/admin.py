# consultations/admin.py

from django.contrib import admin
from .models import Doctor, Appointment, Prescription, Analysis, Consultation

admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Consultation)
admin.site.register(Prescription)
admin.site.register(Analysis)


