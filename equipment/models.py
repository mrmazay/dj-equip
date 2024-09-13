import os

from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class MaintenanceType(models.Model):
    """Модель для хранения типов обслуживания."""
    name = models.CharField(max_length=255, verbose_name='Название типа обслуживания')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name


class Executor(models.Model):
    """Модель для хранения исполнителей."""
    name = models.CharField(max_length=255, verbose_name='Название')
    contact_info = models.TextField(verbose_name='Контактная информация')

    def __str__(self):
        return self.name


class Equipment(models.Model):
    """Модель для хранения информации об оборудовании."""
    STATUS_CHOICES = [
        ('active', 'В эксплуатации'),
        ('inactive', 'Не в эксплуатации'),
    ]
    DEPARTMENT_CHOICES = [
        ('BAL', 'BAL'),
        ('CLIN', 'CLIN'),
        ('Other', 'Другое'),
    ]
    CONDITION_CHOICES = [
        ('new', 'Новое'),
        ('used', 'Б/У'),
    ]

    name = models.CharField(max_length=255, verbose_name='Название')
    model = models.CharField(max_length=255, verbose_name='Модель')
    manufacturer = models.CharField(max_length=255, verbose_name='Производитель')
    serial_number = models.CharField(max_length=255, verbose_name='Серийный номер')
    code = models.CharField(max_length=255, unique=True, verbose_name='Код прибора')
    location = models.CharField(max_length=255, verbose_name='Расположение')
    responsible_person = models.CharField(max_length=255, verbose_name='Ответственное лицо')
    purchase_date = models.DateField(verbose_name='Дата покупки')
    start_date = models.DateField(verbose_name='Дата ввода в эксплуатацию')
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES, verbose_name='Принадлежность к отделу')
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='new', verbose_name='Состояние')
    service_contact = models.CharField(max_length=255, blank=True, verbose_name='Контакт авторизованного сервиса')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name='Статус')
    notes = models.TextField(blank=True, null=True, verbose_name='Примечания')
    version_start = models.DateTimeField(auto_now_add=True, verbose_name='Начало версии')
    version_end = models.DateTimeField(null=True, blank=True, verbose_name='Конец версии')
    is_current = models.BooleanField(default=True, verbose_name='Актуальная запись')

    def __str__(self):
        return f"{self.name} ({self.code})"

    def update_equipment(self, **kwargs):
        """Функция обновления оборудования по правилам SCD второго типа."""
        self.is_current = False
        self.version_end = timezone.now()
        self.save()
        new_equipment = Equipment.objects.create(
            **{field.name: getattr(self, field.name) for field in self._meta.fields if field.name not in ['id', 'is_current', 'version_end']},
            **kwargs
        )
        return new_equipment


class EquipmentMaintenanceType(models.Model):
    """Промежуточная модель для связи оборудования с типами обслуживания."""
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')
    maintenance_type = models.ForeignKey(MaintenanceType, on_delete=models.CASCADE, verbose_name='Тип обслуживания')
    periodicity_months = models.IntegerField(verbose_name='Периодичность (мес)', null=True, blank=True)

    def __str__(self):
        return f"{self.equipment.name} - {self.maintenance_type.name}"

def equipment_document_path(instance, filename):
    """
    Формирует путь для сохранения файла:
    /documents/{equipment_code}/{equipment_code}-{maintenance_type}-{date_performed}.ext
    """
    # Извлекаем необходимые данные из объекта instance
    equipment_code = instance.equipment.code
    maintenance_type = instance.maintenance_type.name
    date_performed = instance.date_performed.strftime('%Y-%m-%d')

    # Формируем имя файла
    filename = f"{equipment_code}-{maintenance_type}-{date_performed}{os.path.splitext(filename)[1]}"

    # Возвращаем путь к файлу
    return os.path.join(f"documents/{equipment_code}/", filename)

class MaintenanceRecord(models.Model):
    """Модель для хранения записей о проведенных обслуживаний."""
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')
    maintenance_type = models.ForeignKey(MaintenanceType, on_delete=models.CASCADE, verbose_name='Тип обслуживания')
    date_performed = models.DateField(verbose_name='Дата проведения')
    executor = models.ForeignKey(Executor, on_delete=models.SET_NULL, null=True, verbose_name='Исполнитель')
    document_name = models.CharField(max_length=255, verbose_name='Название документа')
    documents = models.FileField(upload_to=equipment_document_path, null=True, blank=True, verbose_name='Документы')
    next_maintenance_date = models.DateField(blank=True,null=True, verbose_name='Дата следующего обслуживания')
    description = models.TextField(null=True, blank=True, verbose_name='Описание проведенного обслуживания')
    notes = models.TextField(blank=True, null=True, verbose_name='Примечания')

    def __str__(self):
        return f"{self.equipment.name} - {self.maintenance_type.name}"

    def save(self, *args, **kwargs):
        """Автоматический расчет следующей даты обслуживания на основе периодичности."""
        try:
            equipment_maintenance_type = EquipmentMaintenanceType.objects.get(
                equipment=self.equipment, maintenance_type=self.maintenance_type
            )
            if equipment_maintenance_type.periodicity_months:
                self.next_maintenance_date = self.date_performed + relativedelta(months=equipment_maintenance_type.periodicity_months)
            else:
                self.next_maintenance_date = None  # Периодичность не указана
        except EquipmentMaintenanceType.DoesNotExist:
            self.next_maintenance_date = None  # Если связь не найдена

        super().save(*args, **kwargs)

