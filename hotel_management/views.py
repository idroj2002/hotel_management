from django.shortcuts import render, redirect
from administration.views import reservation_list
from restaurant.views import restaurant_home
from cleaning.views import cleaning_home
from super_user.views import superuser_home


def is_receptionist(user):
    return user.groups.filter(name='Receptionist').exists()


def is_restaurant(user):
    return user.groups.filter(name='Restaurant').exists()


def is_cleaner(user):
    return user.groups.filter(name='Cleaning').exists()


def home(request):
    if request.user.is_superuser:
        return redirect(superuser_home)
    elif is_receptionist(request.user):
        return redirect(reservation_list, reservation_type='hotel')
    elif is_restaurant(request.user):
        return redirect(restaurant_home)
    elif is_cleaner(request.user):
        return redirect(cleaning_home)
    else:
        return render(request, 'not_authorized.html')
