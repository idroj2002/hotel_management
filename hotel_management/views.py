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
    is_superuser = request.user.is_superuser
    is_receptionistuser = is_receptionist(request.user)
    is_restaurantuser = is_restaurant(request.user)
    is_cleaneruser = is_cleaner(request.user)
    is_worker = False
    if is_superuser or is_receptionistuser or is_restaurantuser or is_cleaneruser:
        is_worker = True
    if is_worker:
        return render(request, 'home.html', {'is_worker':is_worker, 'is_receptionist':is_receptionistuser, 'is_restaurant':is_restaurantuser, 'is_cleaner':is_cleaneruser, 'is_superuser':is_superuser})
    else:
        return render(request, 'clients/clients_home.html')

