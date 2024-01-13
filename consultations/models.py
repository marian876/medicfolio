from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from products.models import Product, Specialty

class Doctor(models.Model):
    nombre = models.CharField(max_length=255, verbose_name=_("Nombre del Médico"))
    especialidad = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Especialidad"))
    telefono_personal = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Celular"))
    ubicacion = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Consultorio"))
    telefono_reserva = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Teléfono"))
    notas = models.TextField(blank=True, verbose_name=_("Notas"))
    imagen = models.ImageField(upload_to='doctores/', blank=True, null=True, verbose_name=_("Imagen"))
    
    class Meta:
        verbose_name = ("Doctor")
        verbose_name_plural = ("Doctores")

    def __str__(self):
        return self.nombre

class Appointment(models.Model):
    TYPE_CHOICES = (
        ('consulta', 'Consulta Médica'),
        ('analisis', 'Análisis Médico'),
    )
    tipo = models.CharField(max_length=10, choices=TYPE_CHOICES, default='consulta', verbose_name=_("Tipo de Cita"))
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name=_("Médico"))
    fecha_hora = models.DateTimeField(verbose_name=_("Fecha y Hora"))
    motivo = models.TextField(blank=True, verbose_name=_("Motivo"))
    costo = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name=_("Costo de la Consulta"))
    acompanante = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Acompañante"))
    pendiente = models.BooleanField(default=True, verbose_name=_("Pendiente"))
    cita_posterior = models.PositiveIntegerField(default=0, verbose_name=_("Días para la siguiente cita"))
    nota = models.TextField(blank=True, verbose_name=_("Notas"))

    class Meta:
        verbose_name = _("Cita")
        verbose_name_plural = _("Citas")

    def __str__(self):
        return f"{self.doctor.nombre} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"

class Consultation(models.Model):
    cita = models.OneToOneField(Appointment, on_delete=models.CASCADE, verbose_name=_("Cita"), related_name="consulta")
    audio = models.FileField(upload_to='consultations/audios/', null=True, blank=True, verbose_name=_("Audio de la Consulta"))
    diagnostico = models.CharField(max_length=255, blank=True, verbose_name=_("Diagnóstico"))  
    pdf_indicaciones = models.FileField(upload_to='consultations/prescriptions/', null=True, blank=True, verbose_name=_("PDF de Indicaciones"))
    notas = models.TextField(blank=True, verbose_name=_("Notas de la Consulta"))
    
    class Meta:
        verbose_name = _("Consulta")
        verbose_name_plural = _("Consultas")

    def __str__(self):
        return f"Consulta para {self.cita}"

class Prescription(models.Model):
    consulta = models.ForeignKey(
    'consultations.Consultation',  
    on_delete=models.CASCADE,
    related_name='prescriptions',
    null=False, verbose_name=_("Consulta Relacionada")
    )
    producto = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='prescriptions', 
        verbose_name=_("Producto")
    )
    dosis = models.PositiveIntegerField(verbose_name=_("Dosis diaria"))
    frecuencia = models.CharField(max_length=255, verbose_name=_("Frecuencia"))
    periodo = models.PositiveIntegerField(null=True,blank=True, verbose_name=_("Periodo (días)"))
    periodo_indefinido = models.BooleanField(default=False, verbose_name=_("Periodo Indefinido"))
    activa = models.BooleanField(default=True, verbose_name=_("Activa"))

    def get_absolute_url(self):
        return reverse('consultations:prescription_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Prescripción")
        verbose_name_plural = _("Prescripciones")

    def __str__(self):
        return f"{self.producto.nombre_local} - {self.dosis}"

class Analysis(models.Model):
    consulta = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='analisis', verbose_name=_("Consulta Relacionada"))
    fecha_analisis = models.DateField(verbose_name=_("Fecha del Análisis"))
    descripcion = models.TextField(blank=True, verbose_name=_("Descripción"))
    resultado_pdf = models.FileField(upload_to='analysis/', null=True, blank=True, verbose_name=_("Resultado del Análisis"))
    realizado = models.BooleanField(default=False, verbose_name=_("Realizado"))

    class Meta:
        verbose_name = _("Análisis")
        verbose_name_plural = _("Análisis")

    def __str__(self):
        return f"Análisis para {self.consulta}"