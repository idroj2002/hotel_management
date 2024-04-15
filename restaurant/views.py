from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from administration.models import RestaurantReservation

# Create your views here.

def is_restaurant(user):
    return user.groups.filter(name='Restaurant').exists()


@login_required
def restaurant_home(request):
    if not is_restaurant(request.user):
        from hotel_management.views import home
        return redirect(home)
    
    reservations = RestaurantReservation.objects.all()
    reservation_type = 'restaurant'
    header = 'Reservas de restaurante'
    return render(request, 'reservations.html', {'reservation_type': reservation_type,
                                                 'header': header, 'reservations': reservations})