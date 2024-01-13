from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('citas_pendientes/', views.DashboardAppointmentListView.as_view(), name='dashboard_appointment'),
]
