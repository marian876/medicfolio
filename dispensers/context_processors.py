# dispensers/context_processors.py

from .utils import get_or_create_dispenser

def cart_processor(request):
    dispenser = get_or_create_dispenser(request)
    return {'cart_item_count': dispenser.products.count() if dispenser else 0}
