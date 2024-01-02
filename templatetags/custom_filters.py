from django import template

register = template.Library()

@register.filter(name='price_format')
def price_format(value):
    try:
        # Convertir el valor a flotante
        value = float(value)
        # Formatear el número con separadores de miles y redondeado a 0 decimales
        formatted_value = '{:,.0f}'.format(value)
        # Reemplazar comas por puntos para el formato de miles
        formatted_value = formatted_value.replace(',', '.')
        return '{} Gs.'.format(formatted_value)
    except (ValueError, TypeError):
        return value  # Retorna el valor original si no se puede convertir
