from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from administration.models import RestaurantReservation
from administration.forms import RestaurantReservationForm


# Create your views here.

def is_restaurant(user):
    return user.groups.filter(name='Restaurant').exists()


@login_required
def restaurant_home(request):
    if not is_restaurant(request.user):
        from hotel_management.views import home
        return redirect(home)

    reservations = RestaurantReservation.objects.all()
    return render(request, 'restaurant/reservations.html', {'reservations': reservations})


@login_required
def add_reservation(request):
    if not is_restaurant(request.user):
        from hotel_management.views import home
        return redirect(home)

    if request.method == 'POST':
        form = RestaurantReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant_home')
    else:
        form = RestaurantReservationForm()
    return render(request, 'restaurant/add_reservation_form.html', {'form': form})


@login_required
def reservation_detail(request, reservation_id):
    if not is_restaurant(request.user):
        from hotel_management.views import home
        return redirect(home)

    reservation = get_object_or_404(RestaurantReservation, pk=reservation_id)
    return render(request, 'restaurant/reservation_detail.html', {'reservation': reservation})


@login_required
def edit_reservation(request, reservation_id):
    if not is_restaurant(request.user):
        from hotel_management.views import home
        return redirect(home)

    reservation = get_object_or_404(RestaurantReservation, pk=reservation_id)
    form_model = RestaurantReservationForm
    if request.method == 'POST':
        form = form_model(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation_detail', reservation_id=reservation_id)
    else:
        form = form_model(instance=reservation)
    return render(request, 'restaurant/edit_reservation.html', {'reservation': reservation, 'form': form})


@login_required
def delete_reservation(request, reservation_id):
    if not is_restaurant(request.user):
        from hotel_management.views import home
        return redirect(home)

    reservation = get_object_or_404(RestaurantReservation, pk=reservation_id)
    if request.method == 'POST':
        reservation.cancelled = True
        reservation.save()
        return redirect('restaurant_home')
    return render(request, 'restaurant/delete_reservation.html', {'reservation': reservation})
