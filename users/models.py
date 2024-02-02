from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from consultations.models import Doctor

class User(AbstractUser):
    def get_full_name(self):
        return '{} {}'.format(self.first_name,self.last_name)

class Customer(User):
    class Meta:
        proxy = True
    
    def get_products(self):
        return []
    
class PatientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuario")
    celular = models.CharField("Teléfono", max_length=15)  # Debe ser un número de teléfono
    seguro = models.TextField("Seguro médico", null=True, blank=True)
    medico = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Médico")

    fecha_nacimiento = models.DateField("Fecha de nacimiento", null=True, blank=True)
    encargado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patients', limit_choices_to={'groups__name': 'Familiar'})  # Debe ser uno de los familiares
    alergias = models.TextField("Alergias", default='No especificado', null=True, blank=True)
    enfermedades_base = models.TextField("Enfermedades de base", default='', null=True, blank=True)
    cirugias = models.TextField("Cirugías", default='', null=True, blank=True)
    enfermedades_familiares = models.TextField("Enfermedades familiares", default='', null=True, blank=True)
    historial = models.TextField("Historial", default='', null=True, blank=True)
    foto = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def get_groups(self):
        return self.user.groups.all()

    class Meta:
        verbose_name = "Perfil de Paciente"
        verbose_name_plural = "Perfiles de Pacientes"

class CareProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    celular = models.CharField("Teléfono", max_length=15, null=True, blank=True)  # Debe ser un número de teléfono
    experiencia = models.TextField("Experiencia laboral", default='', null=True, blank=True)
    habilidades = models.TextField("Habilidades", default='', null=True, blank=True)
    educacion = models.TextField("Educación", default='', null=True, blank=True)
    recomendacion= models.TextField("Recomendado por", default='', null=True, blank=True)
    disponibilidad= models.TextField("Disponibilidad", default='', null=True, blank=True)
    comentario=models.TextField("Comentarios", default='', null=True, blank=True)
    foto = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def get_groups(self):
        return self.user.groups.all()

    class Meta:
        verbose_name = "Perfil de Cuidador"
        verbose_name_plural = "Perfiles de Cuidadores"

class FamilyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    paciente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='familiares',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'groups__name': 'Paciente'},
        verbose_name="Paciente"
    )
    celular = models.CharField("Teléfono", max_length=15, null=True, blank=True)  # Debe ser un número de teléfono
    cohabitacion = models.BooleanField("Cohabitación", default=False, null=True, blank=True)  # Debe ser un campo booleano (True o False)

    def get_groups(self):
        return self.user.groups.all()

    class Meta:
        verbose_name = "Perfil de Familiar"
        verbose_name_plural = "Perfiles de Familiares"
        
    def save(self, *args, **kwargs):
        # Asegúrate de que la relación familiar haya sido aprobada en RequestPatient
        if self.paciente:
            solicitud = RequestPatient.objects.filter(solicitante=self.user, paciente=self.paciente, estado=RequestPatient.ESTADO_ACEPTADO).exists()
            if solicitud:
                super(FamilyProfile, self).save(*args, **kwargs)
            else:
                raise ValueError("La relación familiar no ha sido aprobada.")
        else:
            super(FamilyProfile, self).save(*args, **kwargs)


class RequestPatient(models.Model):
    # Estados posibles de la solicitud
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_ACEPTADO = 'aceptado'
    ESTADO_RECHAZADO = 'rechazado'
    ESTADO_FINALIZADO='finalizado'
    ESTADOS_SOLICITUD = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_ACEPTADO, 'Aceptado'),
        (ESTADO_RECHAZADO, 'Rechazado'),
        (ESTADO_FINALIZADO, 'Finalizado'),

    ]

    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='solicitudes_enviadas', 
        on_delete=models.CASCADE
    )
    paciente = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='solicitudes_recibidas', 
        on_delete=models.CASCADE
    )
    parentezco = models.CharField("Parentezco", max_length=100, null=True, blank=True)
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS_SOLICITUD,
        default=ESTADO_PENDIENTE,
    )


    def __str__(self):
        return f"{self.solicitante} solicita a {self.paciente} - Estado: {self.get_estado_display()}"