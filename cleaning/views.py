from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from administration.models import Room, HotelReservation

# Create your views here.

def is_cleaner(user):
    return user.groups.filter(name='Cleaning').exists()


@login_required
def cleaning_home(request):
    if not is_cleaner(request.user):
        from hotel_management.views import home
        return redirect(home)
    
    reservations = HotelReservation.objects.all()
    reservation_type = 'restaurant'
    header = 'Reservas de restaurante'
    return render(request, 'cleaning_home')