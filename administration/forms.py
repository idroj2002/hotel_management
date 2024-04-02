from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import HotelReservation, RestaurantReservation, Room, Table


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
        fields = ['dni', 'name', 'surname', 'date_of_birth', 'email', 'phone', 'check_in_date', 'check_out_date',
                  'num_guests', 'room_type', 'price', 'room_number']


class RestaurantReservationForm(forms.ModelForm):
    class Meta:
        model = RestaurantReservation
        fields = ['name', 'room_number', 'num_people', 'time']


class Room(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'type', 'occupied']


class Table(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['id', 'capcity', 'occupied']
