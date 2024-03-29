#products/models.py

from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
import uuid
from django.db.models import Sum
from django.conf import settings
from django.utils.translation import gettext_lazy as _



class Presentation(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = ("Presentación")
        verbose_name_plural = ("Presentaciones")

    def __str__(self):
        return self.nombre

class Specialty(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = ("Especialidad")
        verbose_name_plural = ("Especialidades")

    def __str__(self):
        return self.nombre

class Product(models.Model):    
    nombre_local = models.CharField("Nombre", max_length=50, unique=True)
    existencia = models.PositiveBigIntegerField("Existencia en Inventario")
    uso_cotidiano=models.BooleanField("Usado actualmente", default=True)
    venta_controlada = models.BooleanField("Venta Controlada", default=False)
    presentacion = models.ForeignKey(Presentation, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad_caja=models.PositiveBigIntegerField("Cantidad por caja", default=1)
    precio = models.PositiveBigIntegerField("Precio", default=0)
    compuesto_principal = models.TextField("Compuesto Principal", max_length=100, blank=True) # Debe ser una lista desplegable
    especialidad = models.ManyToManyField(Specialty, blank=True)
    fabricante = models.CharField("Fabricante", max_length=100, null=True, blank=True)
    pais = models.CharField("País", max_length=50, default='Paraguay', blank=True)

    descripcion = models.TextField("Descripción", blank=True)
    usos = models.TextField("Usos posibles", blank=True)
    posologia = models.TextField("Posología", blank=True)
    embarazo = models.TextField("Embarazo", blank=True)
    lactancia = models.TextField("Lactancia", blank=True)
    contraindicaciones = models.TextField("Contraindicaciones", blank=True)
    precauciones = models.TextField("Precauciones", blank=True)
    reacciones_adversas = models.TextField("Reacciones Adversas", blank=True)
    interacciones = models.TextField("Interacciones", blank=True)

    codigo_barras = models.CharField(max_length=100, unique=True, null=True, blank=True)
    imagen_caja=models.ImageField(upload_to='products/',null=True, blank=True)
    
    slug=models.SlugField(null=True, blank=True, unique=True)
    creado_el = models.DateTimeField("Creado el", auto_now_add=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='productos_creados')

    paciente = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='productos_asociados', 
        verbose_name=_("Paciente")
    )
    @property
    def active_prescriptions(self):
        # Esto asume que existe al menos una prescripción activa para el producto
        return self.prescriptions.filter(activa=True)
    
    @property
    def precio_por_unidad(self):
        return round(self.precio / self.cantidad_caja) if self.cantidad_caja else 0
    
    @property
    def dias_de_cobertura(self):
        """Devuelve la cantidad de días que el stock actual puede cubrir."""
        total_dosis_diaria = self.prescriptions.filter(activa=True).aggregate(
            total_dosis_diaria=Sum('dosis')
        )['total_dosis_diaria'] or 0

        if total_dosis_diaria == 0:
            return 99999  # Representa "infinito"

        return self.existencia // total_dosis_diaria

    @property
    def sobra(self):
        """Devuelve la cantidad de medicamento extra que no completa un día entero."""
        total_dosis_diaria = self.prescriptions.filter(activa=True).aggregate(
            total_dosis_diaria=Sum('dosis')
        )['total_dosis_diaria'] or 0

        if total_dosis_diaria == 0:
            return 0

        return self.existencia % total_dosis_diaria

    class Meta:
        verbose_name = ("Producto")
        verbose_name_plural = ("Productos")

    def __str__(self):
        return self.nombre_local
    
def set_slug(sender,instance, *args, **kwargs): #callback
    if instance.nombre_local and not instance.slug:
        slug=slugify(instance.nombre_local)
        while Product.objects.filter(slug=slug).exists():
            slug=slugify(
                '{}--{}'.format(instance.nombre_local,str(uuid.uuid4())[:8])
            )
        instance.slug=slug
    
pre_save.connect(set_slug,sender=Product)

