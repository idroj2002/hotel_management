from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta
from clients.models import *

class AvailabilityHotelClientsCheckForm(forms.Form):
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
    number_of_guests = forms.ChoiceField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_room_type'})
    )

class AvailabilityRestaurantClientCheckForm(forms.Form):
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

class ProfileClientForm(forms.ModelForm):
    class Meta:
        model = ProfileClient
        fields = ['dni', 'first_name', 'last_name', 'date_of_birth', 'email', 'phone']

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
        }