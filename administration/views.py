from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
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


@login_required
def reservation_detail(request, reservation_type, reservation_id):
    if reservation_type == 'hotel':
        model = get_object_or_404(HotelReservation, pk=reservation_id)
    else:
        model = get_object_or_404(RestaurantReservation, pk=reservation_id)
    return render(request, 'reservation_detail.html', {'reservation_type': reservation_type,
                                                       'reservation_id': reservation_id, 'model': model})


@login_required
def edit_reservation(request, reservation_type, reservation_id):
    if reservation_type == 'hotel':
        reservation = get_object_or_404(HotelReservation, pk=reservation_id)
        form_model = HotelReservationForm
    else:
        reservation = get_object_or_404(RestaurantReservation, pk=reservation_id)
        form_model = RestaurantReservationForm
    if request.method == 'POST':
        form = form_model(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation_detail', reservation_type=reservation_type, reservation_id=reservation_id)
    else:
        form = form_model(instance=reservation)
    return render(request, 'edit_reservation.html', {'reservation_type': reservation_type,
                                                     'reservation_id': reservation_id, 'form': form})


@login_required
def delete_reservation(request, reservation_type, reservation_id):
    if reservation_type == 'hotel':
        reservation = get_object_or_404(HotelReservation, pk=reservation_id)
    else:
        reservation = get_object_or_404(RestaurantReservation, pk=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        return redirect('reservations_list', reservation_type=reservation_type)
    return render(request, 'delete_reservation.html', {'reservation_type': reservation_type,
                                                       'reservation_id': reservation_id, 'reservation': reservation})
