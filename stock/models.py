# stock/models.py
from django.db import models
from products.models import Product

class Farmacia(models.Model):
    nombre = models.CharField(max_length=100)
    web = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    producto = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='compras')
    cantidad = models.PositiveIntegerField()
    fecha_compra = models.DateTimeField(auto_now_add=True)
    lugar_compra = models.ForeignKey(Farmacia, on_delete=models.CASCADE, verbose_name="Lugar de Compra")
    precio_compra = models.DecimalField("Precio de Compra", max_digits=10, decimal_places=0)

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre_local}"
