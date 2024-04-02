from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from administration.models import HotelReservation, RestaurantReservation
from administration.forms import LoginForm, HotelReservationForm, RestaurantReservationForm


def home(request):
    return render(request, 'home.html')


@login_required
def profile(request):
    hotel_reservations = HotelReservation.objects.all()
    restaurant_reservations = RestaurantReservation.objects.all()
    return render(request, 'profile.html',
                  {'hotel_reservations': hotel_reservations, 'restaurant_reservations': restaurant_reservations})


@login_required
def reservation_list(request, reservation_type):
    if reservation_type == 'hotel':
        reservations = HotelReservation.objects.all()
        header = 'Reservas de habitación'
    elif reservation_type == 'restaurant':
        reservations = RestaurantReservation.objects.all()
        header = 'Reservas de restaurante'
    else:
        reservations = []
        header = 'Reservations'
    return render(request, 'reservations.html', {'reservation_type': reservation_type,
                                                 'header': header, 'reservations': reservations})


@login_required
def add_reservation(request, reservation_type):
    if request.method == 'POST':
        if reservation_type == 'hotel':
            form = HotelReservationForm(request.POST)
        else:
            form = RestaurantReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        if reservation_type == 'hotel':
            form = HotelReservationForm()
        else:
            form = RestaurantReservationForm()
    return render(request, 'add_reservation_form.html', {'reservation_type': reservation_type, 'form': form})


def reservation_detail(request, reservation_type, reservation_id):
    if reservation_type == 'hotel':
        model = get_object_or_404(HotelReservation, pk=reservation_id)
    else:
        model = get_object_or_404(RestaurantReservation, pk=reservation_id)
    return render(request, 'reservation_detail.html', {'reservation_type': reservation_type, 'model': model})


@login_required
def edit_hotel_reservation(request, reservation_id):
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
def edit_restaurant_reservation(request, reservation_id):
    reservation = RestaurantReservation.objects.get(pk=reservation_id)  # Cambia RoomReservation por el modelo correcto
    if request.method == 'POST':
        form = RestaurantReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('home')  # Cambia 'home' por la URL de la página principal
    else:
        form = RestaurantReservationForm(instance=reservation)
    return render(request, 'edit_RestaurantReservation.html', {'form': form})
