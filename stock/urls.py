# stock/urls.py

from . import views
from django.urls import path
from .views import get_product_details,agregar_compra

app_name = 'stock'

urlpatterns = [
    path('comprar/', agregar_compra, name='agregar_compra'),
    path('producto_detalle/', get_product_details, name='get-product-details'),

    path('farmacias/', views.PharmacyListView.as_view(), name='pharmacy_list'),
    path('farmacias/add/', views.pharmacy_create_view, name='pharmacy_add'),
    path('farmacias/<int:pk>/edit/', views.pharmacy_update_view, name='pharmacy_edit'),
    path('farmacias/<int:pk>/delete/', views.pharmacy_delete_view, name='pharmacy_delete'),

]
