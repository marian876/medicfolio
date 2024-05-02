from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),

    path('admin/', admin.site.urls),
    path('productos/', include('products.urls')),
    path('retiros/', include('dispensers.urls')),
    path('stock/', include('stock.urls')),
    path('consultas/', include('consultations.urls')),
    path('medicacion/', include('medication.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('usuarios/', include('users.urls')),
    path('calendario/', include('mycalendar.urls')),
    path('mensajes/', include(('messaging.urls', 'messaging'), namespace='messaging')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)