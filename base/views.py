from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HotelReservation, RestaurantReservation
from .forms import LoginForm, HotelReservationForm, RestaurantReservationForm


def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    hotel_reservations = HotelReservation.objects.all()
    restaurant_reservations = RestaurantReservation.objects.all()
    return render(request, 'profile.html', {'hotel_reservations': hotel_reservations, 'restaurant_reservations': restaurant_reservations})

@login_required
def hotel_reservations(request):
    reservations = HotelReservation.objects.all()
    return render(request, 'hotel_reservations.html', {'reservations': reservations})

@login_required
def restaurant_reservations(request):
    reservations = RestaurantReservation.objects.all()
    return render(request, 'restaurant_reservations.html', {'reservations': reservations})

@login_required
def edit_HotelReservation(request, reservation_id):
    reservation = HotelReservation.objects.get(pk=reservation_id)  # Cambia RoomReservation por el modelo correcto
    if request.method == 'POST':
        form = HotelReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('home')  # Cambia 'home' por la URL de la página principal
    else:
        form = HotelReservationForm(instance=reservation)
    return render(request, 'edit_HotelReservation.html', {'form': form})

@login_required
def edit_RestaurantReservation(request, reservation_id):
    reservation = RestaurantReservation.objects.get(pk=reservation_id)  # Cambia RoomReservation por el modelo correcto
    if request.method == 'POST':
        form = RestaurantReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('home')  # Cambia 'home' por la URL de la página principal
    else:
        form = RestaurantReservationForm(instance=reservation)
    return render(request, 'edit_RestaurantReservation.html', {'form': form})