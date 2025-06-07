from django.contrib import admin
from django.urls import path, include
from transport.views import show_routes  # <-- добавь в начало
from blogapp.views import create_superuser_from_web

urlpatterns = [
    path('', show_routes, name='home'),  # <-- добавь это
    path('admin/', admin.site.urls),
    path('transport/', include('transport.urls')),  # явное разделение
    path('routecalc/', include('routecalc.urls')),
    path('create-superuser/', create_superuser_from_web),

]

admin.site.site_header = "Панель администратора"
admin.site.index_title = "Управление Didar Transport Company"
