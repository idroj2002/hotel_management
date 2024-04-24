from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta
from administration.models import HotelReservation, RestaurantReservation, Room, Table, CheckIn


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class AvailabilityCheckForm(forms.Form):
    room_type = forms.ChoiceField(
        choices=[('Ind', 'Individual'), ('Dob', 'Doble'), ('Del', 'Deluxe'), ('Sui', 'Suite')])
    check_in_date = forms.DateField()
    check_out_date = forms.DateField()


class HotelReservationForm(forms.ModelForm):
    class Meta:
        model = HotelReservation
        fields = ['dni', 'first_name', 'last_name', 'date_of_birth', 'email', 'phone',
                  'number_of_guests', 'price', 'room_number', 'cancelled']

        widgets = {
            'dni': forms.TextInput(
                attrs={
                    'placeholder': 'DNI/NIE',
                    'class': 'form-control'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre',
                    'class': 'form-control'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Apellido',
                    'class': 'form-control'
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    'placeholder': 'aaaa-mm-dd',
                    'class': 'form-control'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Correo electrónico',
                    'class': 'form-control'
                }
            ),
            'phone': forms.NumberInput(
                attrs={
                    'placeholder': 'Número de teléfono',
                    'class': 'form-control'
                }
            ),
            'number_of_guests': forms.NumberInput(
                attrs={
                    'placeholder': 'Número de personas',
                    'class': 'form-control'
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'value': 45,
                    'class': 'form-control'
                }
            ),
            'room_number': forms.Select(
                attrs={
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
    check_in_date = forms.DateField(label=_('Check-in Date'))
    check_out_date = forms.DateField(label=_('Check-out Date'))

    class Meta:
        model = RestaurantReservation
        fields = ['name', 'room_number', 'number_of_people', 'time', 'table_id', 'cancelled']

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre de la reserva',
                    'class': 'form-control'
                }
            ),
            'room_number': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'number_of_people': forms.NumberInput(
                attrs={
                    'placeholder': 'Número de personas',
                    'class': 'form-control'
                }
            ),
            'time': forms.DateTimeInput(
                attrs={
                    'value': date.today().strftime('%Y-%m-%d') + '/' + '13:00:00',
                    'class': 'form-control'
                }
            ),
            'table_id': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }

        labels = {
            'name': 'Nombre',
            'room_number': 'Número de habitación',
            'number_of_people': 'Número de comensales',
            'time': 'Turno',
            'table_id': 'Número de mesa',
            'cancelled': 'Cancelada',
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
        fields = ['guests_data', "keys", "cancelled"]

        widgets = {
            'guests_data': forms.Textarea(
                attrs={
                    'placeholder': _('Información del check-in'),
                    'class': 'form-control'
                }
            ),
        }

        labels = {
            'guests_data': 'Información de los huéspedes',
            'keys': 'Llaves entregadas',
            'cancelled': 'Cancelada',
        }
