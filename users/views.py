from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, RequestPatient,PatientProfile, FamilyProfile, CareProfile
from .forms import CareProfileForm, FamilyProfileForm, RegisterForm, UserEditForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirige a los usuarios familiares a seleccionar un paciente
            if 'Familiar' in [group.name for group in user.groups.all()]:
                return redirect('users:request_patient')
            messages.success(request, '¡Registro exitoso!')
            return redirect('index')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

def has_assigned_patient(user):
    if user.groups.filter(name='Familiar').exists():
        return RequestPatient.objects.filter(solicitante=user, estado=RequestPatient.ESTADO_ACEPTADO).exists()
    elif user.groups.filter(name='Cuidador').exists():
        return RequestPatient.objects.filter(solicitante=user, estado=RequestPatient.ESTADO_ACEPTADO).exists()
    return False

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if user.groups.filter(name__in=['Familiar', 'Cuidador']).exists() and not has_assigned_patient(user):
                return redirect('users:request_patient')
            messages.success(request, f'Bienvenido {user.username}')
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña no válidos')

    return render(request, 'users/login.html', {})

@login_required
def request_patient(request):
    user_groups = request.user.groups.values_list('name', flat=True)

    if 'Paciente' in user_groups:
        return redirect('index')

    if request.method == 'POST':
        paciente_id = request.POST.get('paciente_id')
        paciente = get_object_or_404(User, pk=paciente_id)
        RequestPatient.objects.create(solicitante=request.user, paciente=paciente, estado=RequestPatient.ESTADO_PENDIENTE)
        messages.success(request, 'Su solicitud ha sido enviada. Se ha cerrado su sesión.')
        return redirect('index')
    else:
        pacientes_excluidos_ids = RequestPatient.objects.filter(solicitante=request.user).values_list('paciente_id', flat=True)
        pacientes = User.objects.filter(groups__name='Paciente').exclude(id__in=pacientes_excluidos_ids)

        context = {
            'pacientes': pacientes,
            'es_familiar': 'Familiar' in user_groups
        }
        return render(request, 'users/request/request.html', context)

@login_required
def patient_profile_edit(request):
    user = request.user
    profile = getattr(user, 'patientprofile', None)  

    if profile:
        print("Fecha de nacimiento del perfil:", profile.fecha_nacimiento)
    else:
        print("No se encontró perfil de paciente para este usuario.")

    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user, profile_instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = UserEditForm(instance=user, profile_instance=profile)

    return render(request, 'users/profile/patient_edit.html', {'form': form})

@login_required
def family_profile_edit(request):
    user = request.user
    family_profile, created = FamilyProfile.objects.get_or_create(user=user)

    # Solicitudes donde el usuario es el solicitante.
    solicitudes_propias = RequestPatient.objects.filter(
        solicitante=user, 
        estado=RequestPatient.ESTADO_ACEPTADO
    ).select_related('paciente')

    # Solicitudes donde el usuario es el paciente.
    pacientes_ids = RequestPatient.objects.filter(
        paciente=user, 
        estado=RequestPatient.ESTADO_ACEPTADO
    ).values_list('solicitante_id', flat=True)

    solicitudes_al_paciente = RequestPatient.objects.filter(
        solicitante_id__in=pacientes_ids,
        estado=RequestPatient.ESTADO_ACEPTADO
    ).select_related('paciente')

    # Combina las listas y elimina duplicados, si es necesario.
    solicitudes = list(solicitudes_propias) + list(solicitudes_al_paciente)
    # Si es posible que haya duplicados, puedes usar un enfoque más sofisticado para eliminarlos.

    if request.method == 'POST':
        form = FamilyProfileForm(request.POST, instance=family_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = FamilyProfileForm(instance=family_profile)

    return render(request, 'users/profile/family_edit.html', {
        'form': form,
        'solicitudes': solicitudes  # Asegúrate de pasar las solicitudes combinadas aquí
    })


@login_required
def care_profile_edit(request):
    user = request.user
    care_profile = getattr(user, 'careprofile', None)  

    relaciones_aprobadas = RequestPatient.objects.filter(
        solicitante=user, 
        estado=RequestPatient.ESTADO_ACEPTADO
    ).select_related('paciente')

    if request.method == 'POST':
        form = CareProfileForm(request.POST, request.FILES, instance=care_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = CareProfileForm(instance=care_profile)

    return render(request, 'users/profile/care_edit.html', {
    'form': form,
    'relaciones_aprobadas': relaciones_aprobadas,
    'user': user,
    'care_profile': care_profile,
})

def profile_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {
        'user': user,
    }
    return render(request, 'users/profile/patient_view.html', context)

def submit_request(request, paciente_id):
    paciente = get_object_or_404(User, pk=paciente_id)
    RequestPatient.objects.create(solicitante=request.user, paciente=paciente, estado=RequestPatient.ESTADO_PENDIENTE)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'users:view_request'))

@login_required
def accept_request(request, solicitud_id):
    solicitud = get_object_or_404(RequestPatient, pk=solicitud_id)
    if solicitud.paciente == request.user or request.user.has_perm('users.change_requestpatient'):
        solicitud.estado = RequestPatient.ESTADO_ACEPTADO
        solicitud.save()
        messages.success(request, 'La solicitud ha sido aceptada.')
    else:
        messages.error(request, 'No tienes permiso para aceptar esta solicitud.')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'users:view_request'))

def reject_request(request, solicitud_id):
    solicitud = get_object_or_404(RequestPatient, pk=solicitud_id)
    solicitud.estado = RequestPatient.ESTADO_RECHAZADO
    solicitud.save()
    messages.success(request, 'La solicitud ha sido rechazada.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'users:view_request'))

def finish_request(request, solicitud_id):
    solicitud = get_object_or_404(RequestPatient, pk=solicitud_id)
    solicitud.estado = RequestPatient.ESTADO_FINALIZADO
    solicitud.save()
    messages.success(request, 'La solicitud ha sido finalizada.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'users:view_request'))

def family_view_request(request):
    solicitudes_usuario = RequestPatient.objects.filter(solicitante=request.user)
    return render(request, 'users/request/view_family.html', {'solicitudes': solicitudes_usuario})

def view_request(request):
    solicitudes_usuario = RequestPatient.objects.filter(solicitante=request.user)
    return render(request, 'users/request/view_care.html', {'solicitudes': solicitudes_usuario})

def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada con éxito.")
    return redirect('users:login')

@login_required
def patient_view_requests(request):
    # Obtén las solicitudes pendientes
    open_requests = RequestPatient.objects.filter(
        paciente=request.user, 
        estado=RequestPatient.ESTADO_PENDIENTE
    ).select_related('solicitante')

    # Crear un diccionario para asociar cada solicitud con su parentezco
    open_requests_with_relationship = []
    for solicitud in open_requests:
        # Verifica si el solicitante es un familiar
        if solicitud.solicitante.groups.filter(name="Familiar").exists():
            # Obtiene el parentezco si existe
            parentezco = solicitud.parentezco if solicitud.parentezco else "No especificado"
        else:
            parentezco = None  # No mostrar parentezco para no familiares
        open_requests_with_relationship.append({
            'solicitud': solicitud,
            'parentezco': parentezco
        })

    return render(request, 'users/messages.html', {
        'open_requests_with_relationship': open_requests_with_relationship
    })

@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'users/profile/password_change.html'
    
    def get(self, request, *args, **kwargs):
        # Guardar la URL de referencia en la sesión cuando se carga el formulario
        request.session['password_change_referrer'] = request.META.get('HTTP_REFERER', '/')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        # Agregar mensaje de éxito
        messages.success(self.request, 'Tu contraseña ha sido cambiada exitosamente.')
        return response

    def get_success_url(self):
        # Obtener la URL de referencia de la sesión
        return self.request.session.pop('password_change_referrer', '/')