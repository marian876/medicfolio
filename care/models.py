# care/models.py
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Q


class Shift(models.Model):
    RESPONSABLE_CHOICES = [
        ('familiar', 'Familiar'),
        ('cuidador', 'Cuidador'),
        ('enfermera', 'Enfermera'),
    ]

    responsable = models.CharField(max_length=100, choices=RESPONSABLE_CHOICES)
    nombre = models.TextField(blank=True, null=True)
    LUGAR_CHOICES = [
    ('casa', 'Casa'),
    ('sanatorio', 'Sanatorio'),
    ('consulta', 'Consulta'),
    ('salida', 'Salida'),
    ]

    lugar = models.CharField(max_length=100, choices=LUGAR_CHOICES)
    inicio_asignado = models.DateTimeField()
    fin_asignado = models.DateTimeField()
    inicio_real = models.DateTimeField()
    fin_real = models.DateTimeField()
    recordatorio = models.TextField(blank=True, null=True)
    informe = models.TextField(blank=True, null=True)

    def clean(self):
        # Verificar que inicio_asignado es anterior a fin_asignado
        if self.inicio_asignado and self.fin_asignado and self.inicio_asignado > self.fin_asignado:
            raise ValidationError(_('La fecha y hora de inicio no pueden ser posteriores a la fecha y hora de fin.'))
        
        # Validación de superposición de horarios
        overlapping_shifts = Shift.objects.filter(
            Q(responsable=self.responsable) | Q(lugar=self.lugar),
            inicio_asignado__lt=self.fin_asignado,
            fin_asignado__gt=self.inicio_asignado
        ).exclude(pk=self.pk)

        if overlapping_shifts.exists():
            raise ValidationError(_('Existe una superposición de horarios con otro turno.'))

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Shift, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.responsable} ({self.inicio_asignado} - {self.fin_asignado})"
