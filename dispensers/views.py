# dispensers/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import IntegrityError, transaction
from products.models import Product
from dispensers.models import Dispenser, DispenserProducts
from dispensers.utils import get_or_create_dispenser

def dispenser(request):
    dispenser = get_or_create_dispenser(request)
    return render(request, 'dispensers/dispenser.html', {'dispenser': dispenser})

def add(request):
    dispenser = get_or_create_dispenser(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= product.existencia:
        dispenser_product = DispenserProducts.objects.create_or_update_quantity(
            dispenser=dispenser, 
            product=product, 
            quantity=quantity
        )
        messages.success(request, "Producto agregado para retirar")
        return redirect('products:product_list')  # Redirigir a la página de origen o a otra relevante
    else:
        messages.error(request, "Cantidad solicitada excede la existencia.")
        return redirect('products:product_list') 

def remove(request):
    dispenser = get_or_create_dispenser(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))

    dispenser.products.remove(product)
    return redirect('dispensers:dispenser')

def register_withdrawal(request):
    if request.method == 'POST':
        dispenser_instance = get_or_create_dispenser(request)
        
        # Asegúrate de que el objeto Dispenser exista
        if not dispenser_instance.id:
            messages.error(request, "El objeto Dispenser no se pudo encontrar o crear.")
            return redirect('dispensers:dispenser')

        try:
            with transaction.atomic():
                # Asegúrate de que la operación es atómica
                dispenser_instance.register_withdrawal(request.user)
                
                # Comprueba si el objeto Dispenser aún existe antes de eliminarlo
                if Dispenser.objects.filter(id=dispenser_instance.id).exists():
                    dispenser_instance.delete()
                    messages.success(request, 'Retiro registrado exitosamente.')
                else:
                    messages.error(request, "El objeto Dispenser ya no existe.")
        except Exception as e:
            messages.error(request, f"Se produjo un error al procesar tu retiro: {e}")

        return redirect('products:product_list')
    else:
        return redirect('products:product_list')

def modify_quantity_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    dispenser = get_or_create_dispenser(request)
    dispenser_product, created = DispenserProducts.objects.get_or_create(
        dispenser=dispenser, 
        product=product
    )

    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 0))
        if new_quantity <= product.existencia:
            dispenser_product.quantity = new_quantity
            dispenser_product.save()
            messages.success(request, "Cantidad actualizada exitosamente.")
        else:
            messages.error(request, "La cantidad no puede exceder la existencia disponible.")

        return redirect('dispensers:dispenser')

    current_quantity = dispenser_product.quantity if dispenser_product else 0
    context = {
        'product': product, 
        'current_quantity': current_quantity,
        'max_quantity': product.existencia if product.existencia > 0 else 0
    }
    return render(request, 'dispensers/modify.html', context)