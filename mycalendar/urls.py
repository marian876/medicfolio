# mycalendar/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_calendar, name='view_calendar'),
]
