# events/urls.py
from django.urls import path
from .views import about, download_all_materials, event_list, materials_list, event_detail, material_detail

urlpatterns = [
    path('', event_list, name='event_list'),
    path('event/<slug:slug>/', event_detail, name='event_detail'),
    path('event/<slug:slug>/materials/', materials_list, name='materials_list'),
    path('material/<int:pk>/', material_detail, name='material_detail'),
    path('event/<slug:event_slug>/download-all/', download_all_materials, name='download_all_materials'),
    path('about/', about, name='about'),
    path('event/<slug:event_slug>/materials/', materials_list, name='materials_list'),
]
