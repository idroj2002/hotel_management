from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet, Q
from django.utils.translation import gettext_lazy as _
from administration.models import HotelReservation, RestaurantReservation, CheckIn
from administration.forms import LoginForm, HotelReservationForm, RestaurantReservationForm, CheckInForm


def is_receptionist(user):
    return user.groups.filter(name='Receptionist').exists()


@login_required
def reservation_list(request, reservation_type):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    if request.method == 'POST':
        query = ''
        if reservation_type == 'hotel':
            query = request.POST.get('query')
            reservations = []
            if query:
                reservations = HotelReservation.objects.filter(
                    # Aquí puedes agregar los campos en los que deseas buscar coincidencias Puedes usar | (pipe) para
                    # combinar múltiples filtros, lo que busca resultados que coincidan con cualquiera de los campos
                    Q(id__icontains=query) |
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query),
                    cancelled=False
                )
            else:
                reservations = HotelReservation.objects.filter(cancelled=False)
            header = _('Room reservations - Search results for') + ' "' + query + '"'
        elif reservation_type == 'restaurant':
            query = request.POST.get('query')
            reservations = []
            if query:
                reservations = RestaurantReservation.objects.filter(
                    Q(id__icontains=query) |
                    Q(name__icontains=query),
                    cancelled=False
                )
            else:
                reservations = RestaurantReservation.objects.filter(cancelled=False)
            header = _('Restaurant reservations - Search results for') + ' "' + query + '"'
        else:
            reservations = []
            header = _('Reservations')
    else:
        query = ''
        if reservation_type == 'hotel':
            reservations = HotelReservation.objects.filter(cancelled=False)
            header = _('Room reservations')
        elif reservation_type == 'restaurant':
            reservations = RestaurantReservation.objects.filter(cancelled=False)
            header = _('Restaurant reservations')
        else:
            reservations = []
            header = _('Reservations')
    return render(request, 'reception/reservations.html', {'reservation_type': reservation_type, 'query': query,
                                                           'header': header, 'reservations': reservations})


@login_required
def cancelled_reservation_list(request, reservation_type):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    if reservation_type == 'hotel':
        reservations = HotelReservation.objects.filter(cancelled=True)
        header = _('Cancelled room reservations')
    elif reservation_type == 'restaurant':
        reservations = RestaurantReservation.objects.filter(cancelled=True)
        header = _('Cancelled restaurant reservations')
    else:
        reservations = []
        header = _('Reservations')
    return render(request, 'reception/cancelled_reservations.html', {'reservation_type': reservation_type,
                                                                     'header': header, 'reservations': reservations})


@login_required
def add_reservation(request, reservation_type):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    if request.method == 'POST':
        if reservation_type == 'hotel':
            form = HotelReservationForm(request.POST)
        else:
            form = RestaurantReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservations_list', reservation_type=reservation_type)
    else:
        if reservation_type == 'hotel':
            form = HotelReservationForm()
        else:
            form = RestaurantReservationForm()
    return render(request, 'reception/add_reservation_form.html', {'reservation_type': reservation_type, 'form': form})


@login_required
def reservation_detail(request, reservation_type, reservation_id):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    if reservation_type == 'hotel':
        reservation = get_object_or_404(HotelReservation, pk=reservation_id)
    else:
        reservation = get_object_or_404(RestaurantReservation, pk=reservation_id)
    if CheckIn.objects.filter(id=reservation_id).exists():
        check_in = CheckIn.objects.get(id=reservation_id)
    else:
        check_in = 'No'
    return render(request, 'reception/reservation_detail.html', {'reservation_type': reservation_type,
                                                                 'reservation_id': reservation_id,
                                                                 'reservation': reservation,
                                                                 'check_in': check_in})


@login_required
def edit_reservation(request, reservation_type, reservation_id):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    if reservation_type == 'hotel':
        if CheckIn.objects.filter(id=reservation_id).exists():
            raise PermissionDenied(_("It is not possible to delete a reservation with a check-in associated."))
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
    return render(request, 'reception/edit_reservation.html', {'reservation_type': reservation_type,
                                                               'reservation_id': reservation_id, 'form': form})


@login_required
def delete_reservation(request, reservation_type, reservation_id):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    if reservation_type == 'hotel':
        if CheckIn.objects.filter(id=reservation_id).exists():
            raise PermissionDenied(_("It is not possible to delete a reservation with a check-in associated."))
        reservation = get_object_or_404(HotelReservation, pk=reservation_id)
    else:
        reservation = get_object_or_404(RestaurantReservation, pk=reservation_id)
    if request.method == 'POST':
        reservation.cancelled = True
        reservation.save()
        return redirect('reservations_list', reservation_type=reservation_type)
    return render(request, 'reception/delete_reservation.html', {'reservation_type': reservation_type,
                                                                 'reservation_id': reservation_id,
                                                                 'reservation': reservation})


@login_required
def add_check_in(request, reservation_type, reservation_id):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    if reservation_type == 'restaurant':
        raise PermissionDenied(_("It is not possible to create a check-in for a restaurant reservation."))
    reservation = get_object_or_404(HotelReservation, pk=reservation_id)
    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            check_in = form.save(commit=False)
            check_in.id_id = reservation_id
            form.save()
            return redirect('reservation_detail', reservation_type=reservation_type, reservation_id=reservation_id)
    else:
        form = CheckInForm()
    return render(request, 'reception/add_check_in_form.html', {'reservation_type': reservation_type,
                                                                'reservation_id': reservation_id,
                                                                'reservation': reservation,
                                                                'form': form})


@login_required
def edit_check_in(request, reservation_type, reservation_id):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    check_in = get_object_or_404(CheckIn, pk=reservation_id)
    if request.method == 'POST':
        form = CheckInForm(request.POST, instance=check_in)
        if form.is_valid():
            form.save()
            return redirect('reservation_detail', reservation_type=reservation_type, reservation_id=reservation_id)
    else:
        form = CheckInForm(instance=check_in)
    return render(request, 'reception/edit_check_in.html', {'reservation_type': reservation_type,
                                                            'reservation_id': reservation_id, 'form': form})


@login_required
def delete_check_in(request, reservation_type, reservation_id):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    check_in = get_object_or_404(CheckIn, pk=reservation_id)
    if request.method == 'POST':
        check_in.cancelled = True
        check_in.save()
        return redirect('reservations_detail', reservation_type=reservation_type, reservation_id=reservation_id)
    return render(request, 'reception/delete_check_in.html', {'reservation_type': reservation_type,
                                                              'reservation_id': reservation_id, 'check_in': check_in})
