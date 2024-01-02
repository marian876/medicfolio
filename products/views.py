# products/views.py

from typing import Any, Dict
from django.db.models.query import QuerySet
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Product, Presentation, Specialty
from .forms import ProductFilterForm, SpecialtyForm, PresentationForm, ProductForm
from django.contrib import messages

from products import forms

def index(request):
    return render(request, 'index.html')

class ProductListView(ListView):
    template_name = 'products/list.html'
    queryset = Product.objects.all().order_by('nombre_local')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de productos'
        context['products'] = context['product_list']
        return context

class ProductListShortView(ListView):
    template_name = 'products/list_short.html'
    context_object_name = 'products'

    def get_queryset(self):
        especialidad = self.request.GET.get('especialidad')
        sin_existencia = self.request.GET.get('sin_existencia', None)
        uso_cotidiano = self.request.GET.get('uso_cotidiano')
        venta_controlada = self.request.GET.get('venta_controlada')

        queryset = Product.objects.all().order_by('nombre_local')
        if especialidad:
            queryset = queryset.filter(especialidad__nombre=especialidad)
        if sin_existencia == 'on':  
            queryset = queryset.filter(existencia=0)
        if uso_cotidiano:
            queryset = queryset.filter(uso_cotidiano=uso_cotidiano == 'on')
        if venta_controlada:
            queryset = queryset.filter(venta_controlada=venta_controlada == 'on')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ProductFilterForm(self.request.GET or None)
        return context

class ProductDetailView(DetailView):
    model=Product
    template_name='products/product.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        print(context)
        return context
    
class ProductSearchListView(ListView):
    template_name='products/search.html'

    def get_queryset(self):
        query = self.query()
        return Product.objects.filter(
            Q(nombre_local__icontains=query) | 
            Q(especialidad__nombre__icontains=query)
        ).distinct()
    
    def query(self):
        return self.request.GET.get('q')
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['query']=self.query()
        context['count']=context['product_list'].count()
        
        return context

def new_product(request):
    presentaciones = Presentation.objects.all()
    especialidades = Specialty.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('alguna_url')
    else:
        form = ProductForm()

    context = {
        'form': form,
        'presentaciones': presentaciones,
        'especialidades': especialidades,
    }
    return render(request, 'products/new_product.html', context)

def edit_product(request, slug):
    presentaciones = Presentation.objects.all()
    especialidades = Specialty.objects.all()
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:product', slug=product.slug)
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'presentaciones': presentaciones,
        'especialidades': especialidades,
    }
    return render(request, 'products/edit_product.html', context)

def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        product.delete()
        return redirect('products:product_list')
    return render(request, 'products/delete_product.html', {'product': product})

# Presentation
class PresentationListView(ListView):
    model = Presentation
    template_name = 'presentation/list.html'

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
