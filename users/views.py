from django.shortcuts import redirect, render
from django.contrib import messages
from medicfolio.forms import UserEditForm
from django.shortcuts import redirect, render
from django.contrib import messages

def profile_edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            print("Archivos recibidos:", request.FILES)  # Mensaje de depuración
            return redirect('index')
        else:
            print("Formulario no válido:", form.errors)  # Mensaje de depuración
    else:
        form = UserEditForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})
