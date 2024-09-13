# Generated by Django 5.1.1 on 2024-09-12 11:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('model', models.CharField(max_length=255, verbose_name='Модель')),
                ('manufacturer', models.CharField(max_length=255, verbose_name='Производитель')),
                ('serial_number', models.CharField(max_length=255, verbose_name='Серийный номер')),
                ('code', models.CharField(max_length=255, unique=True, verbose_name='Код прибора')),
                ('location', models.CharField(max_length=255, verbose_name='Расположение')),
                ('responsible_person', models.CharField(max_length=255, verbose_name='Ответственное лицо')),
                ('purchase_date', models.DateField(verbose_name='Дата покупки')),
                ('start_date', models.DateField(verbose_name='Дата ввода в эксплуатацию')),
                ('department', models.CharField(choices=[('BAL', 'BAL'), ('CLIN', 'CLIN'), ('Other', 'Другое')], max_length=10, verbose_name='Принадлежность к отделу')),
                ('status', models.CharField(choices=[('active', 'В эксплуатации'), ('inactive', 'Не в эксплуатации')], default='active', max_length=10, verbose_name='Статус')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Примечания')),
                ('version_start', models.DateTimeField(auto_now_add=True, verbose_name='Начало версии')),
                ('version_end', models.DateTimeField(blank=True, null=True, verbose_name='Конец версии')),
                ('is_current', models.BooleanField(default=True, verbose_name='Актуальная запись')),
            ],
        ),
        migrations.CreateModel(
            name='Executor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('contact_info', models.TextField(verbose_name='Контактная информация')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название типа обслуживания')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_performed', models.DateField(verbose_name='Дата проведения')),
                ('document_name', models.CharField(max_length=255, verbose_name='Название документа')),
                ('documents', models.FileField(blank=True, null=True, upload_to='documents/', verbose_name='Документы')),
                ('next_maintenance_date', models.DateField(blank=True, verbose_name='Дата следующего обслуживания')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание проведенного обслуживания')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Примечания')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.equipment', verbose_name='Оборудование')),
                ('executor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='equipment.executor', verbose_name='Исполнитель')),
                ('maintenance_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.maintenancetype', verbose_name='Тип обслуживания')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentMaintenanceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodicity_months', models.IntegerField(blank=True, null=True, verbose_name='Периодичность (мес)')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.equipment', verbose_name='Оборудование')),
                ('maintenance_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.maintenancetype', verbose_name='Тип обслуживания')),
            ],
        ),
    ]
