from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from .forms import ClientRegistrationForm, RouteSearchForm
from .models import Route, Route_custom, Transport, Drivers, Booking, Clients
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm, CustomBookingForm 
from django.db.models import Q
from django.utils.timezone import now
from django.contrib import messages
#карта
from django.shortcuts import render
from .forms import RouteForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from django.contrib import messages






# начало блока бронирования
# функция расчета расстояние принемает два параметра
#def calculate_distance(address1, address2):
    # переменной присваеваем вызов геокодирования из библиотеки pip install geopy
    # для преобразование адреса в кординаты
    # user_agent обезательный параметр чтобы сервис знал кто обращается
 #   geolocator = Nominatim(user_agent="transport_company")
 #   try:
  #      location1 = geolocator.geocode(address1)
   #     location2 = geolocator.geocode(address2)

    #    if location1 and location2:
     #       coords1 = (location1.latitude, location1.longitude)
     #       coords2 = (location2.latitude, location2.longitude)
     #       distance = geodesic(coords1, coords2).km
     #       return distance
     #   else:
     #       return None
   # except Exception as e:
   #     print(f"Ошибка геокодирования: {e}")
   #     return None

@login_required
def create_booking_custom(request):
    if request.method == 'POST':
        form = CustomBookingForm(request.POST)
        if form.is_valid():
            departure_date = form.cleaned_data['departure_date']
            if departure_date < now().date():
                messages.error(request, 'Нельзя выбрать дату в прошлом.')
            else:
                distance = request.POST.get('distance')
                price = request.POST.get('price')

                if not distance or not price:
                    messages.error(request, 'Ошибка: не удалось получить расстояние или цену. Попробуйте ещё раз.')
                    return redirect('create_request')

                route_custom = form.save(commit=False)
                route_custom.price = float(price)
                route_custom.distance = float(distance)  # если поле есть в модели
                route_custom.save()

                client, _ = Clients.objects.get_or_create(user=request.user)
                booking = Booking(
                    client=client,
                    route=None,
                    route_custom=route_custom,
                    departure_date=departure_date,
                )
                booking.save()

                messages.success(
                    request,
                    f'Спасибо! Ваша заявка успешно отправлена. Расстояние: {float(distance):.2f} км, Цена: {float(price):.0f} ₸.'
                )
                return redirect('create_request')
    else:
        form = CustomBookingForm()

    return render(request, 'create_request.html', {'form': form})

@login_required
def create_booking_route(request):
    """Создание бронирования для маршрута из списка"""
    route_id = request.GET.get('route_id')
    route = get_object_or_404(Route, id=route_id)
    error_message = None  # Переменная для ошибки

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            if booking.departure_date < now().date():
                error_message = 'Нельзя выбрать дату в прошлом.'
            else:
                booking.client = request.user.clients
                booking.route = route  # Устанавливаем маршрут
                booking.route_custom = None  # Удаляем кастомный маршрут
                booking.save()
                return render(request, 'create_request_route.html', {
                    'form': BookingForm(), 
                    'success_message': 'Спасибо! Ваша заявка успешно отправлена.',
                })
    else:
        form = BookingForm()

    return render(request, 'create_request_route.html', {'form': form, 'route': route, 'error_message': error_message})

# конец блока бронирования


# начало блока
def show_routes(request):
    # создается форма поиска маршрутов в нее передается запрос
    form = RouteSearchForm(request.GET)
    # еременную созраняем выбор всех записей модели Route 
    routes = Route.objects.all()
    # если форма валидна is_valid встроенный метод Django
    if form.is_valid():
        # в переменную сохраняем только проверенные данные
        query = form.cleaned_data['query']
        if query:
            routes = routes.filter(end_location__icontains=query)
    return render(request, 'show_routes.html', {'routes': routes, 'form': form})

# конец блок


# начало блока регистрация
from django.contrib.auth import login, logout, authenticate
from .forms import ClientRegistrationForm

def register(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически логиним после регистрации
            return redirect('show_routes')
    else:
        form = ClientRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('show_routes')
        else:
            return render(request, 'login.html', {'error': 'Неверные данные'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('show_routes')

# конец блока регистрация

















# начало блока личный кабинет
@login_required
def profile(request):
    # менеджер модели . метод фильтра где имя = имени из запроса
    # filter Возвращает QuerySet — список объектов ятобы работать с объектом используется first
    client = Clients.objects.filter(user=request.user).first()
    # возвращает все заказы если клиента не нашли
    my_booking = client.bookings.all() if client else []
    return render(request, 'profile.html', {'my_booking': my_booking})

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, client=request.user.clients)

    if booking.route_custom:
        FormClass = CustomBookingForm
        instance = booking.route_custom
    else:
        FormClass = BookingForm
        instance = booking

    if request.method == 'POST':
        form = FormClass(request.POST, instance=instance)
        if form.is_valid():
            departure_date = form.cleaned_data['departure_date']

            if departure_date < now().date():
                messages.error(request, 'Нельзя выбрать дату в прошлом.')
            else:
                form.save()

                # Сброс транспорта и водителя
                booking.transport = None
                booking.driver = None
                booking.status = 'В обработке'

                booking.departure_date = departure_date  # Всегда обновляем дату
                booking.save()  # Сохраняем изменения в booking (нужно всегда!)

                return redirect('profile')
    else:
        form = FormClass(instance=instance)

    return render(request, 'edit_booking.html', {'form': form, 'booking': booking})


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, client=request.user.clients)
    
    if request.method == 'POST':
        # Освобождаем ресурсы
        if booking.driver:
            booking.driver.aviable = True
            booking.driver.save()
        if booking.transport:
            booking.transport.aviable = True
            booking.transport.save()

        booking.delete()
        return redirect('profile')

    return render(request, 'delete_booking.html', {'booking': booking})


# начало блока личный кабинет