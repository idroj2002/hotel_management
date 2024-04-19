from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date, timedelta
from administration.models import HotelReservation, RestaurantReservation, Room, Table, CheckIn


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class HotelReservationForm(forms.ModelForm):
    class Meta:
        model = HotelReservation
        fields = ['dni', 'first_name', 'last_name', 'date_of_birth', 'email', 'phone', 'check_in_date', 'check_out_date',
                  'number_of_guests', 'room_type', 'price', 'room_number']
                
        widgets = {
            'dni': forms.TextInput(
                attrs = {
                    'placeholder': 'DNI/NIE',
                    'class': 'form-control'
                }
            ),
            'first_name': forms.TextInput(
                attrs = {
                    'placeholder': 'Nombre',
                    'class': 'form-control'
                }
            ),
            'last_name': forms.TextInput(
                attrs = {
                    'placeholder': 'Apellido',
                    'class': 'form-control'
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs = {
                    'placeholder': 'aaaa-mm-dd',
                    'class': 'form-control'
                }
            ),
            'email': forms.EmailInput(
                attrs = {
                    'placeholder': 'Correo electrónico',
                    'class': 'form-control'
                }
            ),
            'phone': forms.NumberInput(
                attrs = {
                    'placeholder': 'Número de teléfono',
                    'class': 'form-control'
                }
            ),
            'check_in_date': forms.DateInput(
                attrs = {
                    'value': date.today() + timedelta(days=1),
                    'class': 'form-control'
                }
            ),
            'check_out_date': forms.DateInput(
                attrs = {
                    'value': date.today() + timedelta(days=2),
                    'class': 'form-control'
                }
            ),
            'number_of_guests': forms.NumberInput(
                attrs = {
                    'placeholder': 'Número de personas',
                    'class': 'form-control'
                }
            ),
            'room_type': forms.Select(
                attrs = {
                    'class': 'form-select'
                }
            ),
            'price': forms.NumberInput(
                attrs = {
                    'value': 45,
                    'class': 'form-control'
                }
            ),
            'room_number': forms.Select(
                attrs = {
                    'class': 'form-select'
                }
            ),
        }

        labels = {
            'dni': 'Documento de Identidad',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'date_of_birth': 'Fecha de Nacimiento',
            'email': 'Correo Electrónico',
            'phone': 'Teléfono',
            'check_in_date': 'Fecha de Entrada',
            'check_out_date': 'Fecha de Salida',
            'number_of_guests': 'Número de Huéspedes',
            'price': 'Precio',
            'room_number': 'Número de Habitación',
        }


class RestaurantReservationForm(forms.ModelForm):
    class Meta:
        model = RestaurantReservation
        fields = ['name', 'room_number', 'number_of_people', 'time', 'table_id']

        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'placeholder': 'Nombre de la reserva',
                    'class': 'form-control'
                }
            ),
            'room_number': forms.Select(
                attrs = {
                    'class': 'form-select'
                }
            ),
            'number_of_people': forms.NumberInput(
                attrs = {
                    'placeholder': 'Número de personas',
                    'class': 'form-control'
                }
            ),
            'time': forms.DateTimeInput(
                attrs = {
                    'value': date.today().strftime('%Y-%m-%d') + '/' + '13:00:00',
                    'class': 'form-control'
                }
            ),
            'table_id': forms.Select(
                attrs = {
                    'class': 'form-select'
                }
            ),
        }


class Room(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'type', 'occupied']


class Table(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['id', 'capacity', 'occupied']


class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = ['guests_data', "keys"]

        widgets = {
            'guests_data': forms.Textarea(
                attrs={
                    'placeholder': 'Información  del check-in',
                    'class': 'form-control'
                }
            ),
            'keys': forms.BooleanField(),
        }
