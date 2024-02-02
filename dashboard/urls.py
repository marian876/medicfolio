from django.urls import path, include
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
