from equipment.models import Equipment, EquipmentMaintenanceType, MaintenanceType

# Получаем типы обслуживания Wzorcowanie и Sprawdzenie okresowe
wzorcowanie_type = MaintenanceType.objects.get(name='Wzorcowanie')
sprawdzenie_type = MaintenanceType.objects.get(name='Sprawdzenie okresowe')

# Получаем все оборудование, у которого код начинается с "B-TH-"
equipments = Equipment.objects.filter(code__startswith="B-RT-")

# Для каждого такого оборудования добавляем типы обслуживания
for equipment in equipments:
    # Добавляем Wzorcowanie (периодичность 12 месяцев)
    wzorcowanie_exists = EquipmentMaintenanceType.objects.filter(
        equipment=equipment, maintenance_type=wzorcowanie_type
    ).exists()

    if not wzorcowanie_exists:
        EquipmentMaintenanceType.objects.create(
            equipment=equipment,
            maintenance_type=wzorcowanie_type,
            periodicity_months=12  # Периодичность 12 месяцев
        )
        print(f'Добавлен тип обслуживания "Wzorcowanie" для {equipment.name}')

    # Добавляем Sprawdzenie okresowe (периодичность 3 месяца)
    sprawdzenie_exists = EquipmentMaintenanceType.objects.filter(
        equipment=equipment, maintenance_type=sprawdzenie_type
    ).exists()

    if not sprawdzenie_exists:
        EquipmentMaintenanceType.objects.create(
            equipment=equipment,
            maintenance_type=sprawdzenie_type,
            periodicity_months=3  # Периодичность 3 месяца
        )
        print(f'Добавлен тип обслуживания "Sprawdzenie okresowe" для {equipment.name}')
