from django.urls import path
from . import views
from .views import generate_equipment_pdf, import_csv

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('equipments/', views.equipment_list, name='equipment_list'),
]
urlpatterns += [
    path('equipments/<int:pk>/', views.equipment_detail, name='equipment_detail'),
]
urlpatterns += [
    path('equipment-report/', views.generate_equipment_report, name='equipment_report'),
]
urlpatterns += [
    path('maintenance-calendar/', views.generate_maintenance_calendar, name='maintenance_calendar'),
]
urlpatterns += [
    path('equipments/add/', views.equipment_create, name='equipment_create'),
    path('equipments/<int:pk>/edit/', views.equipment_edit, name='equipment_edit'),
    path('equipments/<int:equipment_id>/maintenance/add/', views.maintenance_create, name='maintenance_create'),
    path('maintenance/<int:pk>/edit/', views.maintenance_edit, name='maintenance_edit'),
]
urlpatterns += [
    path('equipments/<int:equipment_id>/generate_pdf/', generate_equipment_pdf, name='generate_equipment_pdf'),
]

urlpatterns += [
    path('import-csv/', import_csv, name='import_csv'),
]