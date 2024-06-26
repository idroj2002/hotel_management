from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta
from administration.models import HotelReservation, RestaurantReservation, Room, Table, CheckIn, CheckOut


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class AvailabilityHotelCheckForm(forms.Form):
    room_type = forms.ChoiceField(
        choices=[('Ind', 'Individual'), ('Dob', 'Doble'), ('Del', 'Deluxe'), ('Sui', 'Suite')],
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_room_type'})
    )
    check_in_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'id': 'id_check_in_date'})
    )
    check_out_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'id': 'id_check_out_date'})
    )


class AvailabilityRestaurantCheckForm(forms.Form):
    number_of_people = forms.IntegerField(label="Número de Personas")
    date = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'id': 'id_date'})
    )
    time = forms.ChoiceField(
        label="Turno",
        choices=[
            ('breakfast_1', 'Desayuno - Primer Turno'),
            ('breakfast_2', 'Desayuno - Segundo Turno'),
            ('lunch_1', 'Comida - Primer Turno'),
            ('lunch_2', 'Comida - Segundo Turno'),
            ('dinner_1', 'Cena - Primer Turno'),
            ('dinner_2', 'Cena - Segundo Turno'),
        ],
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_time'})
    )


class HotelReservationForm(forms.ModelForm):
    class Meta:
        model = HotelReservation
        fields = ['dni', 'first_name', 'last_name', 'date_of_birth', 'email', 'phone',
                  'number_of_guests', 'number_of_nights']

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
                    'class': 'form-control datepicker'
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
            'number_of_nights': forms.NumberInput(
                attrs={
                    'placeholder': 'Número de noches',
                    'class': 'form-control'
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
            'number_of_nights': 'Número de Noches',
            'room_number': 'Número de Habitación',
        }


class RestaurantReservationForm(forms.ModelForm):
    class Meta:
        model = RestaurantReservation
        fields = ['name', 'room_number']

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
        }

        labels = {
            'name': 'Nombre',
            'room_number': 'Número de habitación',
            'number_of_people': 'Número de comensales',
            'date': 'Fecha',
            'time': 'Turno',
            'table_id': 'Número de mesa',
            'cancelled': 'Cancelada',
        }



class RestaurantReservationForm(forms.ModelForm):
    class Meta:
        model = RestaurantReservation
        fields = ['name', 'room_number']

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
        }

        labels = {
            'name': 'Nombre',
            'room_number': 'Número de habitación',
            'number_of_people': 'Número de comensales',
            'date': 'Fecha',
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
        fields = ['guests_data', "keys"]

        widgets = {
            'guests_data': forms.Textarea(attrs={'placeholder': 'Introduzca los nombres completos de los huéspedes y '
                                                                'sus respectivos DNI', 'class': 'form-control'}),
            'keys': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_keys'}),
        }

        labels = {
            'guests_data': 'Información de los huéspedes',
            'keys': 'Llaves entregadas',
        }


class CheckOutForm(forms.ModelForm):
    class Meta:
        model = CheckOut
        fields = ['price', "keys"]

        widgets = {
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'keys': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_keys'}),
        }

        labels = {
            'price': 'Precio total',
            'keys': 'Llaves recogidas',
        }
