# stock/forms.py

from django import forms
from .models import Compra
from .models import Farmacia


class BuyForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['producto', 'cantidad', 'lugar_compra', 'precio_compra'] 

class PharmacyForm(forms.ModelForm):
    class Meta:
        model = Farmacia
        fields = ['nombre', 'web']

class PharmacySearchForm(forms.Form):
    search = forms.CharField(required=False, label='Buscar')
