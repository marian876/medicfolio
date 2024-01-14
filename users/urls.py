# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('usuario/modificar/', views.profile_edit, name='profile_edit'),
]
