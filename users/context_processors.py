from .models import RequestPatient

def open_requests(request):
    if request.user.is_authenticated:
        return {
            'open_requests': RequestPatient.objects.filter(paciente=request.user, estado=RequestPatient.ESTADO_PENDIENTE)
        }
    return {}

def is_patient(request):
    if request.user.is_authenticated:
        return {'is_patient': request.user.groups.filter(name__in=["Paciente", "Administrador"]).exists()}
    return {'is_patient': False}
