from dateutil.relativedelta import relativedelta
from django.db.models import Max
from django.utils import timezone
from .models import MaintenanceRecord, EquipmentMaintenanceType


class MaintenanceService:

    @staticmethod
    def get_upcoming_and_overdue_maintenance(days):
        """Получаем предстоящие и просроченные обслуживания."""
        latest_maintenance = MaintenanceRecord.objects.values('equipment', 'maintenance_type').annotate(
            last_performed=Max('date_performed')
        )

        # Фильтруем предстоящие обслуживания
        upcoming_maintenance = MaintenanceRecord.objects.filter(
            date_performed__in=latest_maintenance.values('last_performed'),
            next_maintenance_date__lte=timezone.now() + relativedelta(days=days)
        ).order_by('next_maintenance_date')

        # Фильтруем просроченные обслуживания
        overdue_maintenance = MaintenanceRecord.objects.filter(
            date_performed__in=latest_maintenance.values('last_performed'),
            next_maintenance_date__lt=timezone.now()
        ).order_by('next_maintenance_date')

        return upcoming_maintenance, overdue_maintenance

    @staticmethod
    def create_maintenance(form, equipment):
        """Создание новой записи обслуживания и связанных задач."""
        maintenance_record = form.save(commit=False)
        maintenance_record.equipment = equipment
        maintenance_record.save()

        # Автоматическое создание техосмотра, если это квалификация
        if maintenance_record.maintenance_type.name == 'qualification' and equipment.technical_inspection_required:
            MaintenanceRecord.objects.create(
                equipment=equipment,
                maintenance_type='technical_inspection',
                date_performed=maintenance_record.date_performed,
                executor=maintenance_record.executor,
                document_name=f"Технический осмотр (связан с квалификацией) - {maintenance_record.document_name}",
                documents=maintenance_record.documents,
                description="Автоматически созданная запись на основе квалификации.",
                next_maintenance_date=maintenance_record.next_maintenance_date,
            )
        return maintenance_record
