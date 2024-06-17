from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from accounting.views import accounting_home, bills_home, taxes_home, offers_home, invoice_pdf, calculate_tourist_tax

urlpatterns = [
    path('', accounting_home, name='accounting_home'),
    path('bills/', bills_home, name='bills'),
    path('bills/pdf/<int:reservation_id>/', invoice_pdf, name="invoice_pdf"),
    path('taxes/', taxes_home, name='taxes'),
    path('calculate_tourist_tax/', calculate_tourist_tax, name='calculate_tourist_tax'),
    path('offers/', offers_home, name='offers'),
]