from django.shortcuts import render, redirect, get_object_or_404
from .models import Message
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings


@login_required
def inbox(request):
        # Limpia todos los mensajes de alerta antes de renderizar la bandeja de entrada
    storage = messages.get_messages(request)
    storage.used = True
    mail_messages = Message.objects.filter(receptor=request.user).order_by('-enviado_el')
    for message in mail_messages:
        message.is_unread = message.leido_el is None
    return render(request, 'messaging/inbox.html', {'mail_messages': mail_messages})


@login_required
def read_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id, receptor=request.user)
    # Marcar el mensaje como leído
    if message.leido_el is None:
        message.leido_el = timezone.now()
        message.save()
    return render(request, 'messaging/read.html', {'message': message})

@login_required
def send_message(request):
    reply_to = request.GET.get('reply_to', None)
    initial_data = {}
    User = get_user_model()  # Usar get_user_model para obtener el modelo de usuario actual

    if reply_to:
        try:
            # Asegúrate de validar que el usuario actual tiene permiso para enviar un mensaje a este usuario
            initial_data['receptor'] = User.objects.get(pk=reply_to)
        except User.DoesNotExist:
            messages.error(request, "Usuario no válido.")
            return redirect('messaging:inbox')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.emisor = request.user  # Asignar el usuario actual como emisor
            message.save()
            messages.success(request, "Mensaje enviado con éxito.")  # Opcional: añadir mensaje de éxito
            return redirect('messaging:inbox')
    else:
        form = MessageForm(initial=initial_data)

    return render(request, 'messaging/send.html', {'form': form})
