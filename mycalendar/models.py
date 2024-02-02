from django.db import models
from django.utils.translation import gettext_lazy as _
from consultations.models import Appointment, Consultation
from django.conf import settings

class CalendarEvent(models.Model):
    titulo = models.CharField(max_length=200, verbose_name=_("Título"))
    descripcion = models.TextField(verbose_name=_("Descripción"), blank=True)
    hora_inicio = models.DateTimeField(verbose_name=_("Hora de inicio"))
    hora_fin = models.DateTimeField(verbose_name=_("Hora de fin"))
    cita = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Cita asociada"))
    consulta = models.ForeignKey(Consultation, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Consulta asociada"))
    paciente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Paciente"), related_name='eventos_calendario')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='eventos_creados', verbose_name=_("Creado por"))

    class Meta:
        verbose_name = _("Evento")
        verbose_name_plural = _("Eventos")

    def __str__(self):
        return self.titulo
