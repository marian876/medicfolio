# care/forms.py

from django import forms
from .models import Turno

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['responsable', 'nombre', 'lugar', 'inicio_asignado', 'fin_asignado', 'inicio_real', 'fin_real', 'recordatorio', 'informe']
