from .models import Dispenser


def get_or_create_dispenser(request):
    user = request.user if request.user.is_authenticated else None
    
    if user:
        # Buscar un Dispenser existente para el usuario autenticado
        dispenser = Dispenser.objects.filter(user=user).first()
        if dispenser:
            # Guardar el dispenser_id en la sesión
            request.session['dispenser_id'] = dispenser.dispenser_id
            return dispenser

    # Proceder como antes si no hay usuario autenticado o no se encontró un Dispenser
    dispenser_id = request.session.get('dispenser_id')
    dispenser = Dispenser.objects.filter(dispenser_id=dispenser_id).first()

    if dispenser is None:
        dispenser = Dispenser.objects.create(user=user)

    request.session['dispenser_id'] = dispenser.dispenser_id
    return dispenser
