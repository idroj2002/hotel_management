from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from clients.views import *

urlpatterns = [
    path('', clients_home, name='clients_home'),
    path('hotel', clients_hotel, name='clients_hotel'),
    path('restaurant', clients_restaurant, name='clients_restaurant'),
    path('profile', clients_profile, name='clients_profile'),
    path('reservations', clients_reservations, name='clients_reservations'),
]