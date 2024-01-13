from . import views
from django.urls import path

app_name='dispensers'

urlpatterns = [
    path('',views.dispenser,name='dispenser'),
    path('agregar',views.add,name='add'),
    path('eliminar',views.remove,name='remove'),
    path('modify/<int:product_id>/', views.modify_quantity_view, name='modify'),
    path('registrar-retiro/', views.register_withdrawal, name='register_withdrawal'),
    path('retirar-varios/', views.add_multiple_products, name='add_multiple'),

]
