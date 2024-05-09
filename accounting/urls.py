from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from accounting.views import accounting_home

urlpatterns = [
    path('', accounting_home, name='accounting_home'),
]