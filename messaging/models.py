from django.db import models
from django.conf import settings

class Message(models.Model):
    emisor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receptor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    motivo = models.CharField(max_length=255)
    cuerpo = models.TextField()
    enviado_el = models.DateTimeField(auto_now_add=True)
    leido_el = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"De {self.emisor} a {self.receptor} - {self.motivo}"

