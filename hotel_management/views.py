from django.shortcuts import render, redirect
from administration.views import reservation_list
from restaurant.views import restaurant_home

def is_receptionist(user):
    return user.groups.filter(name='Receptionist').exists()


def is_restaurant(user):
    return user.groups.filter(name='Restaurant').exists()


def home(request):
    if is_receptionist(request.user):
        return redirect('reservation_list', reservation_type='hotel')
    elif is_restaurant(request.user):
        return redirect(restaurant_home)
    else:
        return render(request, 'not_authorized')