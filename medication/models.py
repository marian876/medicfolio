from django.db import models
from products.models import Product
from consultations.models import Prescription

class ActiveProduct(models.Model):
    producto = models.OneToOneField(Product, on_delete=models.CASCADE)
    prescripcion = models.ForeignKey(Prescription, on_delete=models.SET_NULL, null=True)
    activo = models.BooleanField(default=False)
    recordatorio = models.PositiveIntegerField(default=0)  # Calculated field

    def update_recordatorio(self):
        # Lógica para calcular los días restantes según la prescripción y la existencia del producto
        pass

    def save(self, *args, **kwargs):
        self.active = self.prescripcion is not None and self.prescripcion.activa
        self.update_recordatorio()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.nombre_local} - Activo: {self.active}"
