from .models import Equipment

class ReportService:
    @staticmethod
    def generate_equipment_report(date):
        """Генерация отчета по оборудованию на основе даты покупки."""
        return Equipment.objects.filter(purchase_date__lte=date)
