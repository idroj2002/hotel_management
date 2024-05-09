from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from clients.views import clients_home

urlpatterns = [
    path('', clients_home, name='clients_home'),
]