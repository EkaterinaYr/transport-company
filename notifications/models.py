from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name = "получатель")
    message = models.TextField(verbose_name="Сообщение")
    is_read = models.BooleanField(default=False, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создание")
    
    booking = models.ForeignKey('transport.Booking', on_delete=models.CASCADE, null=True, blank=True)

    
    def __str__(self):
        return f'Уведомление для {self.recipient.username}'
    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
    