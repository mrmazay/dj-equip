from dateutil.relativedelta import relativedelta
from .models import Equipment, MaintenanceRecord, EquipmentMaintenanceType


class CalendarService:
    @staticmethod
    def generate_maintenance_calendar(year):
        """
        Генерация календаря обслуживания для оборудования на указанный год.
        Использует промежуточную модель EquipmentMaintenanceType для получения периодичности обслуживания.
        """
        equipments = Equipment.objects.all()  # Получаем все оборудование
        month_numbers = range(1, 13)

        # Типы обслуживания
        maintenance_types = EquipmentMaintenanceType.objects.all()

        maintenance_calendars = {}
        for maintenance_type in maintenance_types:
            calendar = {}
            for equipment in equipments:
                months_data = {month: [] for month in month_numbers}

                # Для каждого оборудования проверяем, есть ли тип обслуживания в EquipmentMaintenanceType
                equipment_maintenance_type = EquipmentMaintenanceType.objects.filter(
                    equipment=equipment, maintenance_type=maintenance_type.maintenance_type
                ).first()

                if not equipment_maintenance_type:
                    continue

                if equipment_maintenance_type:
                    # Получаем периодичность
                    periodicity = equipment_maintenance_type.periodicity_months

                    # Получаем дату последнего обслуживания
                    last_maintenance = MaintenanceRecord.objects.filter(
                        equipment=equipment,
                        maintenance_type=maintenance_type.maintenance_type
                    ).order_by('-date_performed').first()

                    # Если последнее обслуживание было, берем его дату как базовую, иначе дату ввода в эксплуатацию
                    base_date = last_maintenance.date_performed if last_maintenance else equipment.start_date

                    # Вычисляем будущие даты обслуживания
                    future_dates = CalendarService.calculate_next_maintenance_dates(base_date, periodicity, year)

                    # Распределяем даты по месяцам
                    for future_date in future_dates:
                        if future_date.year == year:
                            months_data[future_date.month].append(future_date)

                calendar[equipment] = months_data

            # Добавляем в общий календарь
            maintenance_calendars[maintenance_type.maintenance_type.name] = {
                'name': maintenance_type.maintenance_type.name,
                'calendar': calendar,
            }

        return maintenance_calendars

    @staticmethod
    def calculate_next_maintenance_dates(last_date, periodicity_months, year):
        """
        Вычисление будущих дат обслуживания на основании последней даты и периодичности.
        """
        dates = []
        current_date = last_date

        while current_date.year <= year:  # Пока год не превышает указанный
            next_date = current_date + relativedelta(months=periodicity_months)
            if next_date.year == year:
                dates.append(next_date)
            current_date = next_date

        return dates
