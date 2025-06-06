from django.urls import path
from .views import create_booking_custom, create_booking_route, show_routes 
from .views import register, login_view, logout_view, profile, edit_booking, delete_booking


urlpatterns = [
    path('', show_routes, name='show_routes'),
    path('create_request/', create_booking_custom, name='create_request'),
    path('create_request_route/', create_booking_route, name='create_request_route'),
    
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    
    path('booking/edit/<int:booking_id>/', edit_booking, name='edit_booking'),
    path('booking/delete/<int:booking_id>/', delete_booking, name='delete_booking'),

]


