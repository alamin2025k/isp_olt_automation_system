# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add-olt/', views.add_olt_device, name='add_olt_device'),
    path('onu-status/', views.onu_status_search, name='onu_status_search'),
    path('offline-onus/', views.offline_onu_list, name='offline_onu_list'),
    path('remove-onu/<int:onu_id>/', views.remove_offline_onu, name='remove_offline_onu'),
    # Add more URLs for MikroTik, device lists, etc.
]
