from django.contrib import admin
from .models import Equipment, MaintenanceRecord, MaintenanceType, Executor, EquipmentMaintenanceType

# Настройка отображения для модели Equipment
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'manufacturer', 'serial_number', 'code', 'status', 'department')
    search_fields = ('name', 'model', 'serial_number', 'code')
    list_filter = ('status', 'department')

# Настройка отображения для модели MaintenanceRecord
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'maintenance_type', 'date_performed', 'executor', 'next_maintenance_date')
    search_fields = ('equipment__name', 'maintenance_type__name', 'executor__name')
    list_filter = ('maintenance_type', 'executor', 'next_maintenance_date')

# Настройка отображения для модели MaintenanceType
class MaintenanceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Настройка отображения для модели Executor
class ExecutorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')
    search_fields = ('name',)

# Настройка отображения для модели EquipmentMaintenanceType
class EquipmentMaintenanceTypeAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'maintenance_type', 'periodicity_months')
    search_fields = ('equipment__name', 'maintenance_type__name')

# Регистрация моделей в админке
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(MaintenanceRecord, MaintenanceRecordAdmin)
admin.site.register(MaintenanceType, MaintenanceTypeAdmin)
admin.site.register(Executor, ExecutorAdmin)
admin.site.register(EquipmentMaintenanceType, EquipmentMaintenanceTypeAdmin)
