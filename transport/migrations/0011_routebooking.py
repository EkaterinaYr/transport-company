# Generated by Django 5.1.2 on 2024-12-07 20:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0010_delete_routeorder'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouteBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('departure_date', models.DateField()),
                ('seats', models.IntegerField()),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('start_route', models.CharField(blank=True, max_length=255, null=True)),
                ('end_route', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('days_count', models.IntegerField(blank=True, null=True)),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.route')),
            ],
        ),
    ]
