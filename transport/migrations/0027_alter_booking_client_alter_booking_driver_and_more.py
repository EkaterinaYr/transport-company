# Generated by Django 5.1.2 on 2025-02-23 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0026_alter_route_end_location_alter_route_number_of_days_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='transport.clients', verbose_name='id клиента'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='transport.drivers', verbose_name='id транспорта'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='route',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='transport.route', verbose_name='id маршрута'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='route_custom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='transport.route_custom', verbose_name='id маршрута_клиента'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='transport',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='transport.transport', verbose_name='id водителя'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Имя улиента'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Фамилия клиента'),
        ),
        migrations.AlterField(
            model_name='drivers',
            name='aviable',
            field=models.BooleanField(max_length=50, verbose_name='Доступностьr'),
        ),
        migrations.AlterField(
            model_name='drivers',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Имя водителя'),
        ),
        migrations.AlterField(
            model_name='drivers',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Фамилия водителя'),
        ),
        migrations.AlterField(
            model_name='drivers',
            name='license_number',
            field=models.CharField(max_length=50, verbose_name='Лицензионый номер'),
        ),
        migrations.AlterField(
            model_name='drivers',
            name='phone_number',
            field=models.CharField(max_length=20, verbose_name='Номе телефона'),
        ),
        migrations.AlterField(
            model_name='route_custom',
            name='end_location',
            field=models.CharField(max_length=255, verbose_name='Конец_маршрута'),
        ),
        migrations.AlterField(
            model_name='route_custom',
            name='number_of_days',
            field=models.IntegerField(blank=True, null=True, verbose_name='Количество_дней'),
        ),
        migrations.AlterField(
            model_name='route_custom',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена_маршрута'),
        ),
        migrations.AlterField(
            model_name='route_custom',
            name='seats',
            field=models.IntegerField(default=0, verbose_name='Количество_пасажиров'),
        ),
        migrations.AlterField(
            model_name='route_custom',
            name='start_location',
            field=models.CharField(max_length=255, verbose_name='Начало_маршрута'),
        ),
        migrations.AlterField(
            model_name='transport',
            name='capacity',
            field=models.PositiveIntegerField(verbose_name='Вместимость'),
        ),
        migrations.AlterField(
            model_name='transport',
            name='model',
            field=models.CharField(max_length=50, verbose_name='Модель'),
        ),
        migrations.AlterField(
            model_name='transport',
            name='technical_condition',
            field=models.CharField(choices=[('Excellent', 'Excellent'), ('Good', 'Good'), ('Satisfactory', 'Satisfactory'), ('Needs Repair', 'Needs Repair')], default='Good', max_length=20, verbose_name='Техническое состояние'),
        ),
        migrations.AlterField(
            model_name='transport',
            name='transport_number',
            field=models.CharField(max_length=20, verbose_name='Номер транспорта'),
        ),
    ]
