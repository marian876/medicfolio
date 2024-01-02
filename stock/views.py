# stock/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import FormularioCompra, FormularioFarmacia
from django.views.generic import ListView
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Farmacia
from django.http import HttpResponseRedirect

def get_product_details(request):
    product_id = request.GET.get('id')
    if product_id:
        product = Product.objects.get(id=product_id)
        return JsonResponse({
            'precio': product.precio,
            'cantidad_caja': product.cantidad_caja,
        })
    return JsonResponse({'error': 'Producto no encontrado'}, status=404)

def agregar_compra(request):
    compra_realizada = False
    form = FormularioCompra()

    if 'producto_id' in request.GET:
        producto = get_object_or_404(Product, pk=request.GET['producto_id'])
        form = FormularioCompra(initial={'producto': producto, 'precio_compra': producto.precio_por_unidad})

    if request.method == 'POST':
        form = FormularioCompra(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            producto = compra.producto

            producto.existencia += compra.cantidad
            # Actualizamos el precio de producto con el precio unitario de compra
            producto.precio = compra.precio_compra  
            producto.save()

            compra.save()
            messages.success(request, 'Compra agregada correctamente.')
            if 'next' in request.POST and request.POST['next']:
                return redirect(request.POST['next'])
            else:
                compra_realizada = True
                form = FormularioCompra()

    context = {
        'form': form,
        'compra_realizada': compra_realizada,
        'next': request.GET.get('next', 'products:product_list_short')
    }
    return render(request, 'stock/buy.html', context)


class PharmacyListView(ListView):
    model = Farmacia
    template_name = 'pharmacy/list.html'
    context_object_name = 'farmacias'

def pharmacy_create_view(request):
    if request.method == 'POST':
        form = FormularioFarmacia(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farmacia agregada con éxito.')
            return redirect('stock:pharmacy_list')
    else:
        form = FormularioFarmacia()
    return render(request, 'pharmacy/create.html', {'form': form})

def pharmacy_update_view(request, pk):
    farmacia = get_object_or_404(Farmacia, pk=pk)
    if request.method == 'POST':
        form = FormularioFarmacia(request.POST, instance=farmacia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farmacia actualizada con éxito.')
            return redirect('stock:pharmacy_list')
    else:
        form = FormularioFarmacia(instance=farmacia)
    return render(request, 'pharmacy/update.html', {'form': form, 'farmacia': farmacia})

def pharmacy_delete_view(request, pk):
    farmacia = get_object_or_404(Farmacia, pk=pk)
    if request.method == 'POST':
        farmacia.delete()
        messages.success(request, 'Farmacia eliminada con éxito.')
        return redirect('stock:pharmacy_list')
    return render(request, 'pharmacy/delete.html', {'farmacia': farmacia})