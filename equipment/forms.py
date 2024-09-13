from django import forms
from .models import Equipment, MaintenanceRecord

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'model', 'manufacturer', 'serial_number', 'code', 'location', 'responsible_person',
                  'purchase_date', 'start_date', 'department', 'condition', 'service_contact', 'status', 'notes']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ['maintenance_type', 'date_performed', 'executor', 'document_name', 'documents',
                  'description', 'next_maintenance_date', 'notes']
        widgets = {
            'date_performed': forms.DateInput(attrs={'type': 'date'}),
            'next_maintenance_date': forms.DateInput(attrs={'type': 'date'}),
        }
