from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta
from administration.models import RestaurantReservation, Table


class RestaurantReservationForm(forms.ModelForm):
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


class Table(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['id', 'capacity', 'occupied']