# stock/forms.py

from django import forms
from .models import Compra
from .models import Farmacia


class FormularioCompra(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['producto', 'cantidad', 'lugar_compra', 'precio_compra'] 

class FormularioFarmacia(forms.ModelForm):
    class Meta:
        model = Farmacia
        fields = ['nombre', 'web']