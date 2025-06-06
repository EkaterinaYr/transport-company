from django import forms
from .models import Route, Route_custom, Transport, Drivers, Booking, Clients
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ClientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Clients.objects.create(
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                phone_number=self.cleaned_data['phone_number'],
                user=user
            )
        return user

class RouteSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Поиск по маршруту', widget=forms.TextInput(attrs={'placeholder': 'Введите город или маршрут'}))

class RouteForm(forms.Form):
    start_address = forms.CharField(label="Начальный адрес",
                                    widget=forms.TextInput(attrs={'id': 'start_address'}))  # Добавляем id
    end_address = forms.CharField(label="Конечный адрес",
                                  widget=forms.TextInput(attrs={'id': 'end_address'}))  # Добавляем id

class BookingForm(forms.ModelForm):
    """Форма для бронирования стандартных маршрутов."""
    class Meta:
        model = Booking
        exclude = ['status', 'client', 'driver', 'transport', 'route_custom', 'route']
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data

class CustomBookingForm(forms.ModelForm):
    start_location = forms.CharField(
        max_length=255,
        required=True,
        label="Начальный пункт"
    )
    end_location = forms.CharField(
        max_length=255,
        required=True,
        label="Конечный пункт"
    )
    seats = forms.IntegerField(
        required=True,
        label="Количество мест"
    )
    departure_date = forms.DateField(
        required=True,
        label="Дата отправления",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Route_custom
        fields = ['start_location', 'end_location', 'seats', 'departure_date']

    def clean(self):
        cleaned_data = super().clean()
        start_location = cleaned_data.get('start_location')
        end_location = cleaned_data.get('end_location')
        seats = cleaned_data.get('seats')
        departure_date = cleaned_data.get('departure_date')

        if not all([start_location, end_location, seats, departure_date]):
            raise forms.ValidationError("Все поля для индивидуального маршрута должны быть заполнены.")

        return cleaned_data

