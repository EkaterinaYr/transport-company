from django.contrib import admin
from .models import Notification
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Notification)
class AdminNotification(admin.ModelAdmin):
    list_display=('message_link', 'is_read', 'created_at')
    list_editable=('is_read', )

    
    def message_link(self, obj):
        if obj.booking:
            url = reverse('admin:transport_booking_change', args=[obj.booking.id])
            return format_html('<a href="{}">{}</a>', url, obj.message)
        return obj.message
    message_link.short_description = "Уведомление"
    
