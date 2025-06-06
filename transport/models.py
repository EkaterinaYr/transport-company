from django.db import models

class Route(models.Model):
    start_location = models.CharField(max_length=255, verbose_name="Начало_маршрута")
    end_location = models.CharField(max_length=255, verbose_name="Конец_маршрута")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена_маршрута")
    number_of_days = models.IntegerField(null=True, blank=True, verbose_name="Количество_дней")
    seats = models.IntegerField(default=0, verbose_name="Количество_пасажиров")
    class Meta:
       verbose_name = "Маршрут"
       verbose_name_plural = "Маршруты"

 
class Route_custom(models.Model):
    start_location = models.CharField(max_length=255, verbose_name="Начало_маршрута")
    end_location = models.CharField(max_length=255, verbose_name="Конец_маршрута")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Цена_маршрута")
    number_of_days = models.IntegerField(null=True, blank=True,  default=1, verbose_name="Количество_дней")
    seats = models.IntegerField(default=0, verbose_name="Количество_пасажиров")
    class Meta:
       verbose_name = "МаршрутПользователя"
       verbose_name_plural = "МаршрутыПользователей"
       
class Transport(models.Model):
    transport_number = models.CharField(max_length=20, verbose_name="Номер транспорта")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость")
    model = models.CharField(max_length=50, verbose_name="Модель")  # New field for the transport model
    TECHNICAL_CONDITIONS = [
        ('Excellent', 'Отличное'),
        ('Needs Repair', 'Требует ремонта'),
    ]
    technical_condition = models.CharField(
        max_length=20, 
        choices=TECHNICAL_CONDITIONS, 
        default='Good',
        verbose_name="Техническое состояние"
    )

    def __str__(self):
        return f"{self.transport_number} ({self.capacity})"
    class Meta:
       verbose_name = "Транспорт"
       verbose_name_plural = "Транспорты"
       
class Drivers(models.Model):
    
    first_name = models.CharField(max_length=100, verbose_name="Имя водителя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия водителя")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    license_number = models.CharField(max_length=50, verbose_name="Лицензионный номер")
    aviable = models.BooleanField(max_length=50, verbose_name="Доступность")

    def __str__(self):
        return f"{self.first_name} ({self.last_name})"
    class Meta:
       verbose_name = "Водитель"
       verbose_name_plural = "Водители"

from django.contrib.auth.models import User

class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="clients")
    first_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия клиента")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
       verbose_name = "Клиент"
       verbose_name_plural = "Клиенты"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('В обработке', 'В обработке'),
        ('Одобрено', 'Одобрено'),
        ('Завершено', 'Завершено'),
        ('Отказано', 'Отказано'),
    ]

    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name="bookings", verbose_name="id клиента")  # Клиент
    transport = models.ForeignKey(Transport, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings", verbose_name="id транспорта")  # Транспорт
    driver = models.ForeignKey(Drivers, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings", verbose_name="id водителя")  # Водитель

    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings", verbose_name="id маршрута")  # Маршрут из списка
    route_custom = models.ForeignKey(Route_custom, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings", verbose_name="id маршрута_клиента")  # Индивидуальный маршрут

    departure_date = models.DateField()  # Дата отправления

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='В обработке',
        verbose_name="Статус"
    )

    def __str__(self):
        return f"{self.client.first_name} {self.client.last_name} - {self.get_route_display()} - {self.status}"

    def get_route_display(self):
        if self.route:
            return f"{self.route.start_location} to {self.route.end_location}"
        elif self.route_custom:
            return f"{self.route_custom.start_location} to {self.route_custom.end_location} (Custom)"
        return "Маршрут не указан"
    class Meta:
       verbose_name = "Заказ"
       verbose_name_plural = "Заказы"



