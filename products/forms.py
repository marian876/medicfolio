# products/forms.py

from django import forms
from .models import Specialty, Presentation, Product
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from medication.models import ActiveProduct


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'nombre_local', 'existencia', 'venta_controlada', 'uso_cotidiano', 
            'presentacion', 'cantidad_caja', 'precio', 'especialidad', 'compuesto_principal',
            'descripcion', 'usos', 'posologia', 'embarazo',
            'lactancia', 'contraindicaciones', 'precauciones', 'reacciones_adversas',
            'interacciones', 'fabricante', 'pais', 'codigo_barras', 'imagen_caja'
        ]
        widgets = {
            'nombre_local': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'existencia': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '9999'}),
            'venta_controlada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'uso_cotidiano': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'presentacion': forms.Select(attrs={'class': 'form-control'}),
            'cantidad_caja': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '999'}),
            'especialidad': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'compuesto_principal': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'usos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'posologia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'embarazo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'lactancia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contraindicaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precauciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'reacciones_adversas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'interacciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fabricante': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '100'}),
            'imagen_caja': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('nombre_local', css_class='form-group col-md-6 mb-0'),
                Column('existencia', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('venta_controlada', css_class='form-group col-md-6 mb-0'),
                Column('uso_cotidiano', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('presentacion', css_class='form-group col-md-6 mb-0'),
                Column('cantidad_caja', css_class='form-group col-md-6 mb-0'),
            ),
            'precio',
            'especialidad',
            Row(
                Column('compuesto_principal', css_class='form-group col-12 mb-0'),
                Column('descripcion', css_class='form-group col-12 mb-0'),
            ),
            Row(
                Column('usos', css_class='form-group col-12 mb-0'),
                Column('posologia', css_class='form-group col-12 mb-0'),
            ),
            Row(
                Column('embarazo', css_class='form-group col-12 mb-0'),
                Column('lactancia', css_class='form-group col-12 mb-0'),
            ),
            Row(
                Column('contraindicaciones', css_class='form-group col-12 mb-0'),
                Column('precauciones', css_class='form-group col-12 mb-0'),
            ),
            Row(
                Column('reacciones_adversas', css_class='form-group col-12 mb-0'),
                Column('interacciones', css_class='form-group col-12 mb-0'),
            ),
            Row(
                Column('fabricante', css_class='form-group col-md-6 mb-0'),
                Column('pais', css_class='form-group col-md-6 mb-0'),
            ),
            'codigo_barras',
            'imagen_caja'
        )

class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ['nombre']

class PresentationSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar'})
    )
    
class SpecialtyForm(forms.ModelForm):
    class Meta:
        model = Specialty
        fields = ['nombre']

class SpecialtySearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar'})
    )

class ProductFilterForm(forms.Form):
    con_prescripcion = forms.BooleanField(required=False, label="Con prescripción")
    uso_cotidiano = forms.BooleanField(required=False, label='En uso')
    venta_controlada = forms.BooleanField(required=False, label='Venta Controlada')
    sin_existencia = forms.BooleanField(required=False, label='Sin Existencia')
    especialidad = forms.ModelChoiceField(
        queryset=Specialty.objects.all(),
        required=False,
        label="Especialidad",
        empty_label="Cualquier especialidad"
    )
    def __init__(self, *args, **kwargs):
        super(ProductFilterForm, self).__init__(*args, **kwargs)
        self.fields['con_prescripcion'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['uso_cotidiano'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['venta_controlada'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['sin_existencia'].widget.attrs.update({'class': 'form-check-input'})

class ProductSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar'}))