# Generated by Django 5.1.2 on 2024-12-09 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0018_driverschedule_departure_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driverschedule',
            name='departure_date',
        ),
    ]
