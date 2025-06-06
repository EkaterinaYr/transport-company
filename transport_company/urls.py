from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('transport/', include('transport.urls')),  # явное разделение
    path('routecalc/', include('routecalc.urls')),
]

admin.site.site_header = "Панель администратора"
admin.site.index_title = "Управление Didar Transport Company"
