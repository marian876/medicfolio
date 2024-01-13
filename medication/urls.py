from django.urls import path
from . import views

app_name = 'medication'

urlpatterns = [
    path('productos-activos/', views.ActiveProductListView.as_view(), name='medication_list'),
    path('exportar_productos_pdf/', views.export_products_pdf, name='export_products_pdf'),

]
