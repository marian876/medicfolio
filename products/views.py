# products/views.py

from typing import Any, Dict
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.shortcuts import render
from .filters import ProductFilter
from django_filters.views import FilterView

from .filters import ProductFilter
from .models import Product, Presentation, Specialty
from .forms import ProductFilterForm, SpecialtyForm, SpecialtySearchForm, PresentationForm, PresentationSearchForm, ProductForm, ProductSearchForm
from medication.models import ActiveProduct
from consultations.models import Prescription
from django.db.models import Exists, OuterRef


def index(request):
    return render(request, 'index.html')

class ProductListView(FilterView):
    model = Product
    filterset_class = ProductFilter
    template_name = 'products/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_form = ProductFilterForm(self.request.GET or None)

        if filter_form.is_valid():
            if filter_form.cleaned_data.get('sin_existencia'):
                queryset = queryset.filter(existencia=0)
            if filter_form.cleaned_data.get('uso_cotidiano'):
                queryset = queryset.filter(uso_cotidiano=True)
            if filter_form.cleaned_data.get('venta_controlada'):
                queryset = queryset.filter(venta_controlada=True)
            if filter_form.cleaned_data.get('con_prescripcion'):
                prescripciones_activas = Prescription.objects.filter(
                    producto=OuterRef('pk'),
                    activa=True
                )
                queryset = queryset.filter(Exists(prescripciones_activas))

        # Búsqueda
        self.search_form = ProductSearchForm(self.request.GET or None)
        if self.search_form.is_valid() and self.search_form.cleaned_data.get('search'):
            search_query = self.search_form.cleaned_data.get('search')
            queryset = queryset.filter(
                Q(nombre_local__icontains=search_query) |
                Q(descripcion__icontains=search_query) |
                Q(compuesto_principal__icontains=search_query) |
                Q(fabricante__icontains=search_query) |
                Q(pais__icontains=search_query) |
                Q(codigo_barras__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ProductFilterForm(self.request.GET or None)
        context['search_form'] = ProductSearchForm(self.request.GET or None)
        return context
    
class ProductListShortView(ListView):
    model = Product
    template_name = 'products/list_short.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Filtra inicialmente por uso_cotidiano=True
        queryset = Product.objects.filter(uso_cotidiano=True).order_by('nombre_local')
        self.filter_form = ProductFilterForm(self.request.GET or None)

        if self.filter_form.is_valid():
            if self.filter_form.cleaned_data.get('con_prescripcion'):
                prescripciones_activas = Prescription.objects.filter(
                    producto=OuterRef('pk'),
                    activa=True
                )
                queryset = queryset.annotate(
                    tiene_prescripcion_activa=Exists(prescripciones_activas)
                ).filter(tiene_prescripcion_activa=True)

            if self.filter_form.cleaned_data.get('sin_existencia'):
                queryset = queryset.filter(existencia=0)
            
            if self.filter_form.cleaned_data.get('venta_controlada'):
                queryset = queryset.filter(venta_controlada=True)

        self.search_form = ProductSearchForm(self.request.GET or None)
        if self.search_form.is_valid() and self.search_form.cleaned_data.get('search'):
            search_query = self.search_form.cleaned_data['search']
            queryset = queryset.filter(
                Q(nombre_local__icontains=search_query) |
                Q(descripcion__icontains=search_query) |
                Q(compuesto_principal__icontains=search_query) |
                Q(fabricante__icontains=search_query) |
                Q(pais__icontains=search_query) |
                Q(codigo_barras__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        context['search_form'] = self.search_form
        return context

class ProductDetailView(DetailView):
    model=Product
    template_name='products/product.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['specialty_names'] = [specialty.nombre for specialty in context['product'].especialidad.all()]
        return context
    
def new_product(request):
    presentaciones = Presentation.objects.all()
    especialidades = Specialty.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            form.save_m2m()  # Esto guardará las relaciones ManyToMany como 'especialidad'
            messages.success(request, "Producto agregado correctamente.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = ProductForm()

    context = {
        'form': form,
        'presentaciones': presentaciones,
        'especialidades': especialidades,
    }
    return render(request, 'products/create.html', context)

def edit_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    presentaciones = Presentation.objects.all()
    especialidades = Specialty.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            form.save_m2m()
            messages.success(request, "Producto actualizado correctamente.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'presentaciones': presentaciones,
        'especialidades': especialidades,
    }
    return render(request, 'products/update.html', context)

def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        product.delete()
        return redirect('products:product_list')
    return render(request, 'products/delete.html', {'product': product})

class PresentationListView(ListView):
    model = Presentation
    template_name = 'presentation/list.html'  
    context_object_name = 'presentations'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('search', '')  # Asegúrate de usar 'search' si así lo nombraste en el input del formulario
        if search_term:
            queryset = queryset.filter(nombre__icontains=search_term)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = PresentationSearchForm(self.request.GET or None)
        return context

def presentation_create(request):
    form = PresentationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Presentación agregada correctamente.")
        return redirect('products:presentation_list')
    return render(request, 'presentation/create.html', {'form': form})

def presentation_update(request, pk):
    presentation = get_object_or_404(Presentation, pk=pk)
    form = PresentationForm(request.POST or None, instance=presentation)
    if form.is_valid():
        form.save()
        messages.success(request, "Presentación actualizada correctamente.")
        return redirect('products:presentation_list')
    return render(request, 'presentation/update.html', {'form': form, 'presentation': presentation})

def presentation_delete(request, pk):
    presentation = get_object_or_404(Presentation, pk=pk)
    if request.method == 'POST':
        presentation.delete()
        messages.success(request, "Presentación eliminada correctamente.")
        return redirect('products:presentation_list')
    return render(request, 'presentation/delete.html', {'presentation': presentation})

# Specialty
class SpecialtyListView(ListView):
    model = Specialty
    template_name = 'specialty/list.html'
    context_object_name = 'specialties'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('search', '')  # Asegúrate de usar 'search' si así lo nombraste en el input del formulario
        if search_term:
            queryset = queryset.filter(nombre__icontains=search_term)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SpecialtySearchForm(self.request.GET or None)
        return context

def specialty_create(request):
    form = SpecialtyForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Especialidad agregada correctamente.")
        return redirect('products:specialty_list')
    return render(request, 'specialty/create.html', {'form': form})

def specialty_update(request, pk):
    specialty = get_object_or_404(Specialty, pk=pk)
    form = SpecialtyForm(request.POST or None, instance=specialty)
    if form.is_valid():
        form.save()
        messages.success(request, "Especialidad actualizada correctamente.")
        return redirect('products:specialty_list')
    return render(request, 'specialty/update.html', {'form': form, 'specialty': specialty})

def specialty_delete(request, pk):
    specialty = get_object_or_404(Specialty, pk=pk)
    if request.method == 'POST':
        specialty.delete()
        messages.success(request, "Especialidad eliminada correctamente.")
        return redirect('products:specialty_list')
    return render(request, 'specialty/delete.html', {'specialty': specialty})
