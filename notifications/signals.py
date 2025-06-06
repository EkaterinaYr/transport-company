from transport.models import Booking  # Импортируем Booking из приложения transport
from notifications.models import Notification  # Импортируем Notification из текущего приложения
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_delete

from django.contrib.auth.models import User

#встроенные декодер принемает встроенный сигнал (возникает при сохранение объекта в БД) и связавает с нашей моделью
@receiver(post_save, sender=Booking)
#параметры следующие: наша модель, определенная запись, булевое значение, доп.параметры
def notify_about_order(sender, instance, created, **kwargs):
    # если создан объект created истина только если объет только создан 
    if created:
        # выбераем всех пользователей со статусом админестратора
        admins = User.objects.filter(is_staff=True)
        for admin in admins:
            # создаем уведомление модель.менеджер для работы с БД. создаем запись()
            Notification.objects.create(
                recipient=admin,
                message=f"Создан новый заказ от {instance.client.user}",
                booking=instance
            )
    else:
        # выбераем всех пользователей со статусом админестратора
        admins = User.objects.filter(is_staff=True)
        for admin in admins:
            # создаем уведомление модель.менеджер для работы с БД. создаем запись()
            Notification.objects.create(
                recipient=admin,
                message=f"Изменен заказ от {instance.client.user}",
                booking=instance
            )


from django.db.models.signals import pre_delete

@receiver(pre_delete, sender=Booking)
def notify_about_order_deleted(sender, instance, **kwargs):
    admins = User.objects.filter(is_staff=True)
    for admin in admins:
        Notification.objects.create(
            recipient=admin,
            message=f"Заказ {instance.id} будет удалён",
            booking=instance 
        )
