from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from consultations.models import Prescription
from products.models import Product
from .models import ActiveProduct

@receiver(post_save, sender=Prescription)
@receiver(post_delete, sender=Prescription)
def update_product_status(sender, instance, **kwargs):
    product = instance.producto
    active_prescriptions = Prescription.objects.filter(producto=product, activa=True).exists()

    if active_prescriptions:
        ActiveProduct.objects.update_or_create(
            producto=product,
            defaults={'activo': True, 'prescripcion': instance}
        )
    else:
        ActiveProduct.objects.filter(producto=product).update(activo=False, prescripcion=None)

    # Actualizar el campo uso_cotidiano en el modelo Product
    Product.objects.filter(id=product.id).update(uso_cotidiano=active_prescriptions)
