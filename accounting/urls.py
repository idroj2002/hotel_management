from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from accounting.views import accounting_home, bills_home, taxes_home, offers_home

urlpatterns = [
    path('', accounting_home, name='accounting_home'),
    path('bills/', bills_home, name='bills'),
    path('taxes/', taxes_home, name='taxes'),
    path('offers/', offers_home, name='offers'),
]