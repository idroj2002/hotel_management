"""
URL configuration for base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from restaurant.views import restaurant_home, add_reservation, reservation_detail, edit_reservation, \
    delete_reservation, cancelled_reservation_list, bill_list, edit_bill, add_to_cart, complete_reservation, \
    cart_resume, modify_cart, set_paid


urlpatterns = [
    path('', restaurant_home, name='restaurant_home'),
    path('reservation_detail/<int:reservation_id>/', reservation_detail, name='reservation_detail'),
    path('add_reservation/', add_reservation, name='add_reservation'),
    path('edit_reservation/<int:reservation_id>/', edit_reservation, name='edit_reservation'),
    path('delete_reservation/<int:reservation_id>/', delete_reservation, name='delete_reservation'),
    path('cancelled_reservations/', cancelled_reservation_list, name='cancelled_reservations_list'),
    path('bills/', bill_list, name='restaurant_bills'),
    path('bills/edit/<int:reservation_id>/', edit_bill, name='edit_bill'),
    path('bills/cart/<int:reservation_id>/', cart_resume, name='cart_resume'),
    path('bills/add_to_cart/', add_to_cart, name='add_to_cart'),
    path('bills/modify_cart/', modify_cart, name='modify_cart'),
    path('bills/set_paid_true/<int:reservation_id>/', set_paid, {'paid': True}, name='set_paid_true'),
    path('bills/set_paid_false/<int:reservation_id>/', set_paid, {'paid': False}, name='set_paid_false'),   
    path('complete_reservation/', complete_reservation, name='complete_reservation'),
]
