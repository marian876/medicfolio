# users/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path('usuario/login', views.login_view, name='login'),
    path('usuario/logout', views.logout_view, name='logout'),
    path('usuario/registro', views.register, name='register'),
    path('paciente/modificar/', views.patient_profile_edit, name='patient_profile_edit'),
    path('familiar/modificar/', views.family_profile_edit, name='family_profile_edit'),
    path('cuidador/modificar/', views.care_profile_edit, name='care_profile_edit'),
    path('finalizar_solicitud/<int:solicitud_id>/', views.finish_request, name='finish_request'),

    path('usuario/ver/<int:user_id>/', views.profile_view, name='profile_view'),


    path('solicitar_paciente/', views.request_patient, name='request_patient'),
    path('enviar_solicitud/<int:paciente_id>/', views.submit_request, name='submit_request'),
    path('aceptar_solicitud/<int:solicitud_id>/', views.accept_request, name='accept_request'),
    path('rechazar_solicitud/<int:solicitud_id>/', views.reject_request, name='reject_request'),
    path('solicitud/', views.view_request, name='view_request'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)