from django.urls import path
from .views import inbox, read_message, send_message

urlpatterns = [
    path('enviar/', send_message, name='send_message'),
    path('bandeja/', inbox, name='inbox'),
    path('mensajes/<int:message_id>/', read_message, name='read_message'),
]
