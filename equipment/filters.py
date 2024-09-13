import django_filters
from .models import Equipment

class EquipmentFilter(django_filters.FilterSet):
    class Meta:
        model = Equipment
        fields = {
            'name': ['icontains'],
            'model': ['icontains'],
            'manufacturer': ['icontains'],
            'department': ['exact'],
            'status': ['exact'],
        }
