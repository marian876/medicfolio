from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
    # URLs para Doctor
    path('doctores/', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctores/nuevo/', views.doctor_create_view, name='doctor_create'),
    path('doctores/<int:pk>/editar/', views.doctor_update_view, name='doctor_update'),
    path('doctores/<int:pk>/eliminar/', views.doctor_delete, name='doctor_delete'),
    path('doctores/<int:pk>/', views.doctor_detail_view, name='doctor_detail'),

    # URLs para Appointment
    path('citas/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('citas/nueva/', views.appointment_create_view, name='appointment_create'),
    path('citas/<int:pk>/editar/', views.appointment_update_view, name='appointment_update'),
    path('citas/<int:pk>/eliminar/', views.appointment_delete_view, name='appointment_delete'),
    path('citas/<int:pk>', views.appointment_detail_view, name='appointment_detail'),

    # URLs para Prescription
    path('prescripcion/', views.PrescriptionListView.as_view(), name='prescription_list'),
    path('prescripcion/nueva/', views.prescription_create_view, name='prescription_create'),
    path('prescripcion/<int:pk>/editar/', views.prescription_update_view, name='prescription_update'),
    path('prescripcion/<int:pk>/eliminar/', views.prescription_delete_view, name='prescription_delete'),
    path('prescripcion/<int:pk>/', views.prescription_detail_view, name='prescription_detail'),

    path('consultas/lista/', views.ConsultationListView.as_view(), name='consultation_list'),
    path('consultas/nueva/', views.consultation_create_view, name='consultation_create'),
    path('consultas/<int:pk>/editar/', views.consultation_update_view, name='consultation_update'),
    path('consultas/<int:pk>/eliminar/', views.consultation_delete_view, name='consultation_delete'),
    path('consultas/<int:pk>/', views.consultation_detail_view, name='consultation_detail'),

    path('analisis/lista/', views.AnalysisListView.as_view(), name='analysis_list'),
    path('analisis/nuevo/', views.analysis_create_view, name='analysis_create'),
    path('analisis/<int:pk>/editar/', views.analysis_update_view, name='analysis_update'),
    path('analisis/<int:pk>/eliminar/', views.analysis_delete_view, name='analysis_delete'),
    path('analisis/<int:pk>/', views.analysis_detail_view, name='analysis_detail'),


]

