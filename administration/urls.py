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
from administration.views import reservation_list, add_reservation, reservation_detail, edit_reservation,\
    delete_reservation, add_check_in, edit_check_in, delete_check_in, cancelled_reservation_list, complete_reservation

urlpatterns = [
    path('reservations/<str:reservation_type>/', reservation_list, name='reservations_list'),
    path('reservations/add/<str:reservation_type>/', add_reservation, name='add_reservation'),
    path('reservations/detail/<str:reservation_type>/<int:reservation_id>/', reservation_detail,
         name='reservation_detail'),
    path('reservations/edit/<str:reservation_type>/<int:reservation_id>/', edit_reservation,
         name='edit_reservation'),
    path('reservations/delete/<str:reservation_type>/<int:reservation_id>/', delete_reservation,
         name='delete_reservation'),
    path('reservations/add_check_in/<str:reservation_type>/<int:reservation_id>/', add_check_in,
         name='add_check_in'),
    path('reservations/edit_check_in/<str:reservation_type>/<int:reservation_id>/', edit_check_in,
         name='edit_check_in'),
    path('reservations/delete_check_in/<str:reservation_type>/<int:reservation_id>/', delete_check_in,
         name='delete_check_in'),
    path('reservations/cancelled_reservations/<str:reservation_type>/', cancelled_reservation_list,
         name='cancelled_reservations_list'),
    path('reservations/complete_reservation/<str:reservation_type>/',complete_reservation,
         name='complete_reservation'),
]
