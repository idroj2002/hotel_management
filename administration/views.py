import datetime

from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet, Q
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from urllib.parse import urlencode, parse_qs
from administration.models import HotelReservation, RestaurantReservation, CheckIn, Room, Table, CheckOut
from administration.forms import LoginForm, HotelReservationForm, RestaurantReservationForm, CheckInForm, \
    AvailabilityRestaurantCheckForm, AvailabilityHotelCheckForm, CheckOutForm


def is_receptionist(user):
    return user.groups.filter(name='Receptionist').exists()


@login_required
def reservation_list(request, reservation_type):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    query = '-1'
    check_ins = []
    check_outs = []
    if request.method == 'POST':
        if reservation_type == 'hotel':
            query = request.POST.get('query')
            reservations = HotelReservation.objects.filter(
                Q(id__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query),
                cancelled=False
            )
            reservations = []
            if query:
                reservations = HotelReservation.objects.filter(
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
            reservations = RestaurantReservation.objects.filter(
                Q(id__icontains=query) |
                Q(name__icontains=query),
                cancelled=False
            )
            header = _('Restaurant reservations - Search results for') + ' "' + query + '"'
        else:
            reservations = []
            header = _('Reservations')
    else:
        if reservation_type == 'hotel':
            today = datetime.datetime.now().date()
            check_ins = HotelReservation.objects.filter(check_in_date=today, cancelled=False)
            check_outs = HotelReservation.objects.filter(check_out_date=today, cancelled=False)
            reservations = HotelReservation.objects.filter(cancelled=False).order_by('-id')
            header = _('Room reservations')
        elif reservation_type == 'restaurant':
            reservations = RestaurantReservation.objects.filter(cancelled=False)
            header = _('Restaurant reservations')
        else:
            reservations = []
            header = _('Reservations')
    return render(request, 'reception/reservations.html', {'reservation_type': reservation_type, 'query': query,
                                                           'header': header, 'reservations': reservations,
                                                           'check_ins': check_ins, 'check_outs': check_outs})


@login_required
def cancelled_reservation_list(request, reservation_type):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    query = '-1'
    if request.method == 'POST':
        if reservation_type == 'hotel':
            query = request.POST.get('query')
            reservations = HotelReservation.objects.filter(
                Q(id__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query),
                cancelled=True
            )
            header = _('Cancelled room reservations - Search results for') + ' "' + query + '"'
        elif reservation_type == 'restaurant':
            query = request.POST.get('query')
            reservations = RestaurantReservation.objects.filter(
                Q(id__icontains=query) |
                Q(name__icontains=query),
                cancelled=True
            )
            header = _('Cancelled restaurant reservations - Search results for') + ' "' + query + '"'
        else:
            reservations = []
            header = _('Cancelled reservations')
    else:
        if reservation_type == 'hotel':
            reservations = HotelReservation.objects.filter(cancelled=True)
            header = _('Cancelled room reservations')
        elif reservation_type == 'restaurant':
            reservations = RestaurantReservation.objects.filter(cancelled=True)
            header = _('Cancelled restaurant reservations')
        else:
            reservations = []
            header = _('Cancelled reservations')
    return render(request, 'reception/cancelled_reservations.html', {'reservation_type': reservation_type,
                                                                     'header': header, 'query': query,
                                                                     'reservations': reservations})


@login_required
def reservation_detail(request, reservation_type, reservation_id):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    check_in = False
    check_out = False
    reservation_editable = True
    check_in_editable = True
    if reservation_type == 'hotel':
        reservation = get_object_or_404(HotelReservation, pk=reservation_id)
        if reservation.cancelled:
            reservation_editable = False
        else:
            today = datetime.datetime.now().date()
            if CheckIn.objects.filter(id=reservation_id).exists():
                check_in = CheckIn.objects.get(id=reservation_id)
                reservation_editable = False
            else:
                if reservation.check_in_date <= today:
                    check_in = True
            if CheckOut.objects.filter(id=reservation_id).exists():
                check_out = CheckOut.objects.get(id=reservation_id)
                check_in_editable = False
            else:
                if check_in is not True and reservation.check_out_date <= today:
                    check_out = True
    else:
        reservation = get_object_or_404(RestaurantReservation, pk=reservation_id)
        if reservation.cancelled:
            reservation_editable = False

    return render(request, 'reception/reservation_detail.html', {'reservation_type': reservation_type,
                                                                 'reservation_id': reservation_id,
                                                                 'reservation': reservation,
                                                                 'reservation_editable': reservation_editable,
                                                                 'check_in_editable': check_in_editable,
                                                                 'check_in': check_in, 'check_out': check_out})


@login_required
def edit_reservation(request, reservation_type, reservation_id):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    if reservation_type == 'hotel':
        if CheckIn.objects.filter(id=reservation_id).exists():
            raise PermissionDenied(_("It is not possible to edit a reservation with a check-in associated."))
        reservation = get_object_or_404(HotelReservation, pk=reservation_id)

        form_model = HotelReservationForm
    else:
        reservation = get_object_or_404(RestaurantReservation, pk=reservation_id)
        form_model = RestaurantReservationForm
    if reservation.cancelled:
        raise PermissionDenied(_("It is not possible to edit a cancelled reservation."))
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
    if reservation.cancelled:
        raise PermissionDenied(_("It is not possible to edit a cancelled reservation."))
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
        raise PermissionDenied(_("It is not possible to create a Check-In for a restaurant reservation."))
    reservation = get_object_or_404(HotelReservation, pk=reservation_id)
    if reservation.cancelled:
        raise PermissionDenied(_("It is not possible to add a check-in for a cancelled reservation."))
    today = datetime.datetime.now().date()
    if reservation.check_in_date > today:
        raise PermissionDenied(_("The date for this Check-in has not been reached yet."))
    if CheckIn.objects.filter(id=reservation_id).exists():
        raise PermissionDenied(_("Already exists a Check-In for this reservation."))
    if CheckOut.objects.filter(id=reservation_id).exists():
        raise PermissionDenied(_("Exists a Check-Out for this reservation so it is closed."))
    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            check_in = form.save(commit=False)
            check_in.id_id = reservation_id
            check_in.created_by = request.user
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

    reservation = get_object_or_404(HotelReservation, pk=reservation_id)
    check_in = get_object_or_404(CheckIn, pk=reservation_id)
    if CheckOut.objects.filter(id=reservation_id).exists():
        raise PermissionDenied(_("Exists a Check-Out for this reservation so it is closed."))
    if request.method == 'POST':
        form = CheckInForm(request.POST, instance=check_in)
        if form.is_valid():
            check_in = form.save(commit=False)
            check_in.created_by = request.user
            form.save()
            return redirect('reservation_detail', reservation_type=reservation_type, reservation_id=reservation_id)
    else:
        form = CheckInForm(instance=check_in)
    return render(request, 'reception/edit_check_in.html', {'reservation_type': reservation_type,
                                                            'reservation_id': reservation_id,
                                                            'reservation': reservation, 'form': form})


@login_required
def delete_check_in(request, reservation_type, reservation_id):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    check_in = get_object_or_404(CheckIn, pk=reservation_id)
    if request.method == 'POST':
        check_in.cancelled = True
        check_in.save()
        return redirect('reservation_detail', reservation_type=reservation_type, reservation_id=reservation_id)
    return render(request, 'reception/delete_check_in.html', {'reservation_type': reservation_type,
                                                              'reservation_id': reservation_id, 'check_in': check_in})


@login_required
def add_check_out(request, reservation_type, reservation_id):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    if reservation_type == 'restaurant':
        raise PermissionDenied(_("It is not possible to create a Check-Out for a restaurant reservation."))
    reservation = get_object_or_404(HotelReservation, pk=reservation_id)
    today = datetime.datetime.now().date()
    if reservation.check_out_date > today:
        raise PermissionDenied(_("The date for this Check-Out has not been reached yet."))
    if CheckOut.objects.filter(id=reservation_id).exists():
        raise PermissionDenied(_("Exists a Check-Out for this reservation so it is closed."))
    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            check_out = form.save(commit=False)
            check_out.id_id = reservation_id
            check_out.created_by = request.user
            form.save()
            return redirect('reservation_detail', reservation_type=reservation_type, reservation_id=reservation_id)
    else:
        form = CheckOutForm()
    return render(request, 'reception/add_check_out_form.html', {'reservation_type': reservation_type,
                                                                 'reservation_id': reservation_id,
                                                                 'reservation': reservation,
                                                                 'form': form})


def save_hotel_reservation(reservation_form, check_in_date, check_out_date, room_type):
    reservation = reservation_form.save(commit=False)
    reservation.check_in_date = check_in_date
    reservation.check_out_date = check_out_date
    reservation.room_type = room_type
    reservation.save()


@login_required
def add_reservation(request, reservation_type):
    if not is_receptionist(request.user):
        from hotel_management.views import home
        return redirect(home)

    if request.method == 'POST':
        if reservation_type == 'hotel':
            availability_form = AvailabilityHotelCheckForm(request.POST)
            if availability_form.is_valid():
                check_in_date = availability_form.cleaned_data['check_in_date']
                check_out_date = availability_form.cleaned_data['check_out_date']
                room_type = availability_form.cleaned_data['room_type']
                data = {'check_in_date': check_in_date, 'check_out_date': check_out_date, 'room_type': room_type}
                data_string = urlencode(data)
                redirect_url = '/administration/reservations/complete_reservation/hotel/?{}'.format(data_string)
                return redirect(redirect_url, reservation_type=reservation_type)

        else:
            availability_form = AvailabilityRestaurantCheckForm(request.POST)
            if availability_form.is_valid():
                number_of_people = availability_form.cleaned_data['number_of_people']
                date = availability_form.cleaned_data['date']
                time = availability_form.cleaned_data['time']
                data = {'number_of_people': number_of_people, 'date': date, 'time': time}
                data_string = urlencode(data)
                redirect_url = '/administration/reservations/complete_reservation/restaurant/?{}'.format(data_string)
                return redirect(redirect_url, reservation_type=reservation_type)

    else:
        if reservation_type == 'hotel':
            availability_form = AvailabilityHotelCheckForm()
        else:
            availability_form = AvailabilityRestaurantCheckForm()
        return render(request, 'reception/availability_form.html', {'reservation_type': reservation_type, 'availability_form': availability_form})


def get_available_rooms(check_in_date, check_out_date, room_type):
    overlapping_reservations = HotelReservation.objects.filter(
        Q(check_in_date__lt=check_out_date) & Q(check_out_date__gt=check_in_date), cancelled=False
    )
    occupied_rooms = [reservation.room_number for reservation in overlapping_reservations]
    all_rooms = Room.objects.filter(type=room_type)
    available_rooms = all_rooms.exclude(id__in=[room.id for room in occupied_rooms])
    return available_rooms


def get_available_tables(number_of_people, date, time):
    overlapping_reservations = RestaurantReservation.objects.filter(
        Q(date=date) & Q(time=time), cancelled=False
    )
    occupied_tables = [reservation.table_id for reservation in overlapping_reservations]
    all_tables = Table.objects.filter(capacity__gte=number_of_people)
    available_tables = all_tables.exclude(id__in=[table.id for table in occupied_tables])
    return available_tables


@login_required
def complete_reservation(request, reservation_type):
    data_string = request.META['QUERY_STRING']
    data = parse_qs(data_string)
    if reservation_type == 'hotel':
        check_in_date = data.get('check_in_date', [''])[0]
        check_out_date = data.get('check_out_date', [''])[0]
        room_type = data.get('room_type', [''])[0]
        available_rooms = get_available_rooms(check_in_date, check_out_date, room_type)
    else:
        number_of_people = data.get('number_of_people', [''])[0]
        date = data.get('date', [''])[0]
        time = data.get('time', [''])[0]
        available_tables = get_available_tables(number_of_people, date, time)

    if request.method == 'POST':
        if reservation_type == 'hotel':
            room_id = request.POST.get('room')
            room = get_object_or_404(Room, pk=room_id)
            reservation_form = HotelReservationForm(request.POST)
            if reservation_form.is_valid():
                reservation = reservation_form.save(commit=False)
                reservation.room_number = room
                reservation.check_in_date = check_in_date
                reservation.check_out_date = check_out_date
                reservation.save()
                return render(request, 'reception/reservation_confirmation.html', {'reservation_type': reservation_type, 'room_id': room.number})
        else:
            table_id = request.POST.get('table')
            table = get_object_or_404(Table, pk=table_id)
            reservation_form = RestaurantReservationForm(request.POST)
            if reservation_form.is_valid():
                reservation = reservation_form.save(commit=False)
                reservation.table_id = table
                reservation.date = date
                reservation.number_of_people = number_of_people
                reservation.time = time
                reservation.save()
                return render(request, 'reception/reservation_confirmation.html', {'reservation_type': reservation_type, 'table_id': table.id})
    else:
        if reservation_type == 'hotel':
            reservation_form = HotelReservationForm()
            return render(request, 'reception/add_reservation_form.html', {
                'reservation_type': reservation_type,
                'reservation_form': reservation_form,
                'available_rooms': available_rooms
            })
        else:
            reservation_form = RestaurantReservationForm()
            return render(request, 'reception/add_reservation_form.html', {
                'reservation_type': reservation_type,
                'reservation_form': reservation_form,
                'available_tables': available_tables
            })
