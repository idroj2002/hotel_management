from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from super_user.views import superuser_home

urlpatterns = [
    path('', superuser_home, name='home'),
]