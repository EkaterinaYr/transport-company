from django.contrib import admin
from .models import Route, Route_custom, Transport, Drivers, Booking, Clients
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import timedelta

admin.site.register(Route_custom)

admin.site.register(Clients)

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('start_location', 'end_location', 'seats')
    orders = ['end_location','seats']
   
@admin.register(Drivers)
class DriversAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'aviable')
   
@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ('transport_number', 'capacity', 'technical_condition')
    orders = ['seats', 'technical_condition']
    list_editable = ('technical_condition', )
    list_per_page = 5


class BookingAdminForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = self.instance
        if not instance:
            return

        departure_date = instance.departure_date
        number_of_days = 1
        seats_needed = None

        if instance.route:
            seats_needed = instance.route.seats
            number_of_days = instance.route.number_of_days
        elif instance.route_custom:
            seats_needed = instance.route_custom.seats
            number_of_days = instance.route_custom.number_of_days

        # Фильтрация доступных водителей
        drivers_qs = Drivers.objects.filter(aviable=True)

        # Фильтрация доступного транспорта по техническому состоянию и вместимости
        transport_qs = Transport.objects.exclude(technical_condition='Needs Repair')
        if seats_needed:
            transport_qs = transport_qs.filter(capacity__gte=seats_needed)

        if departure_date:
            start_date = departure_date
            end_date = departure_date + timedelta(days=number_of_days - 1)

            # Находим пересекающиеся брони
            overlapping_bookings = Booking.objects.filter(
                departure_date__lte=end_date
            ).exclude(pk=instance.pk)

            busy_drivers = set()
            busy_transports = set()

            for booking in overlapping_bookings:
                b_days = booking.route.number_of_days if booking.route else booking.route_custom.number_of_days
                b_end = booking.departure_date + timedelta(days=b_days - 1)
                if b_end >= start_date:
                    if booking.driver:
                        busy_drivers.add(booking.driver.id)
                    if booking.transport:
                        busy_transports.add(booking.transport.id)

            drivers_qs = drivers_qs.exclude(id__in=busy_drivers)
            transport_qs = transport_qs.exclude(id__in=busy_transports)

        # Назначаем отфильтрованные QuerySet-ы
        self.fields['driver'].queryset = drivers_qs
        self.fields['transport'].queryset = transport_qs






@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    form = BookingAdminForm

    def save_model(self, request, obj, form, change):
        # Получаем предыдущий статус (если редактируем существующую заявку)
        old_obj = None
        if obj.pk:
            old_obj = Booking.objects.get(pk=obj.pk)

        # Если статус сменился
        if old_obj and old_obj.status != obj.status:
            # Если заявка одобрена — занять ресурсы
            if obj.status == 'Одобрено':
                if obj.driver:
                    obj.driver.aviable = False
                    obj.driver.save()
                if obj.transport:
                    obj.transport.aviable = False
                    obj.transport.save()

            # Если заявка отказана — освободить ресурсы
            elif obj.status == 'Отказано':
                if obj.driver:
                    obj.driver.aviable = True
                    obj.driver.save()
                if obj.transport:
                    obj.transport.aviable = True
                    obj.transport.save()

        super().save_model(request, obj, form, change)


