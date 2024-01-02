from . import views
from django.urls import path

app_name = 'products'

urlpatterns = [
    path('search', views.ProductSearchListView.as_view(), name='search'),
    path('list/', views.ProductListView.as_view(), name='product_list'),
    path('listshort/', views.ProductListShortView.as_view(), name='product_list_short'),

    path('new', views.new_product, name='new_product'),  
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product'),
    path('<slug:slug>/edit', views.edit_product, name='edit_product'),
    path('<slug:slug>/delete', views.delete_product, name='delete_product'),

    path('presentations/', views.PresentationListView.as_view(), name='presentation_list'),
    path('presentations/add/', views.presentation_create, name='presentation_add'),
    path('presentations/<int:pk>/edit/', views.presentation_update, name='presentation_edit'),
    path('presentations/<int:pk>/delete/', views.presentation_delete, name='presentation_delete'),

    path('specialties/', views.SpecialtyListView.as_view(), name='specialty_list'),
    path('specialties/add/', views.specialty_create, name='specialty_add'),
    path('specialties/<int:pk>/edit/', views.specialty_update, name='specialty_edit'),
    path('specialties/<int:pk>/delete/', views.specialty_delete, name='specialty_delete'),
]
