from django.views.generic import ListView
from django.shortcuts import render
from consultations.models import Appointment

class DashboardAppointmentListView(ListView):
    model = Appointment
    template_name = 'dashboard/snippets/appointment.html'
    context_object_name = 'appointments_active'

    def get_queryset(self):
        return Appointment.objects.filter(pendiente=True).order_by('fecha_hora')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for appointments_active in context['appointments_active']:
            print(appointments_active)
        
        return context

