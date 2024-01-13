from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def get_full_name(self):
        return '{} {}'.format(self.first_name,self.last_name)

class Customer(User):
    class Meta:
        proxy = True
    
    def get_products(self):
        return []
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuario")
    historial = models.TextField("Historial", default='')
    fecha_nacimiento = models.DateField("Fecha de nacimiento", null=True, blank=True)
    encargado = models.TextField("Encargado", default='')
    alergias = models.TextField("Alergias", default='No especificado')
    enfermedades_base = models.TextField("Enfermedades de base", default='')
    cirugias = models.TextField("Cirugías", default='')
    enfermedades_familiares = models.TextField("Enfermedades familiares", default='')
    foto = models.ImageField(upload_to='profiles/', null=True, blank=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"