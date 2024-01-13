from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('usuarios/login', views.login_view, name='login'),
    path('usuarios/logout', views.logout_view, name='logout'),
    path('usuarios/registro', views.register_view, name='register'),

    path('admin/', admin.site.urls),
    path('productos/', include('products.urls')),
    path('retiros/', include('dispensers.urls')),
    path('stock/', include('stock.urls')),
    path('consultas/', include('consultations.urls')),
    path('medicacion/', include('medication.urls')),

]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)