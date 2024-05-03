import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet, Q
from django.utils.translation import gettext_lazy as _
from datetime import datetime, time
from django.http import HttpResponse
from urllib.parse import urlencode, parse_qs
from restaurant.models import RestaurantBill, RestaurantItem, ShoppingCart
from administration.models import RestaurantReservation, Table
from administration.forms import RestaurantReservationForm, AvailabilityRestaurantCheckForm


def is_restaurant(user):
    return user.groups.filter(name='Restaurant').exists()


@login_required
def restaurant_home(request):
    if not is_restaurant(request.user):
        from hotel_management.views import home
        return redirect(home)

    query = '-1'
    query = request.POST.get('query')
    if query:
        reservations = RestaurantReservation.objects.filter(
            Q(id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query),
            cancelled=False
        )
    else:
        reservations = RestaurantReservation.objects.filter(cancelled=False)
    return render(request, 'restaurant/reservations.html', {'reservations': reservations})


@login_required
def cancelled_reservation_list(request):
    if not is_restaurant(request.user):
        from hotel_management.views import home
        return redirect(home)

    query = '-1'
    if request.method == 'POST':
        query = request.POST.get('query')
        reservations = RestaurantReservation.objects.filter(
            Q(id__icontains=query) |
            Q(name__icontains=query),
            cancelled=True
        )
        header = _('Cancelled restaurant reservations - Search results for') + ' "' + query + '"'
    else:
        reservations = RestaurantReservation.objects.filter(cancelled=True)
        header = _('Cancelled restaurant reservations')
    return render(request, 'restaurant/cancelled_reservations.html', {'query': query,
                                                                     'reservations': reservations})


@login_required
def add_reservation(request):
    if not is_restaurant(request.user):
        from hotel_management.views import home
        return redirect(home)

    if request.method == 'POST':
        availability_form = AvailabilityRestaurantCheckForm(request.POST)
        if availability_form.is_valid():
            number_of_people = availability_form.cleaned_data['number_of_people']
            date = availability_form.cleaned_data['date']
            time = availability_form.cleaned_data['time']
            data = {'number_of_people': number_of_people, 'date': date, 'time': time}
            data_string = urlencode(data)
            redirect_url = '/restaurant/complete_reservation/?{}'.format(data_string)
            return redirect(redirect_url)
    else:
        availability_form = AvailabilityRestaurantCheckForm()
        return render(request, 'restaurant/availability_form.html', {'availability_form': availability_form})


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


@login_required
def bill_list(request):
    if not is_restaurant(request.user):
        from hotel_management.views import home
        return redirect(home)
    
    current_time = datetime.now()

    # Define restaurant shifts
    morning_start = time(5, 0, 0)
    afternoon_start = time(12, 0, 0) 
    night_start = time(18, 0, 0)

    next_bills = RestaurantReservation.objects.filter(date__gte=current_time.date())

    today_bills = next_bills.filter(date=current_time.date())

    if current_time.time() > morning_start and current_time.time() < afternoon_start:
        bills = (today_bills.filter(time="breackfast_1") | today_bills.filter(time="breackfast_2")).order_by('-time')
        shift = _('Morning shift')
    elif current_time.time() > afternoon_start and current_time.time() < night_start:
        bills = (today_bills.filter(time="lunch_1") | today_bills.filter(time="lunch_2")).order_by('-time')
        shift = _('Afternoon shift')
    else:
        bills = (today_bills.filter(time="dinner_1") | today_bills.filter(time="dinner_2")).order_by('-time')
        shift = _('Night shift')
    
    bills_ids = bills.values('id')
    other_bills = next_bills.exclude(id__in=bills_ids)

    return render(request, 'restaurant/bills_list.html', {'bills': bills, 'other_bills': other_bills, 'shift': shift})


@login_required
def edit_bill(request, reservation_id):
    if not is_restaurant(request.user):
        from hotel_management.views import home
        return redirect(home)

    items = RestaurantItem.objects.all()
    return render(request, 'restaurant/bill_detail.html', {'items': items, 'reservation_id': reservation_id})


@login_required
def add_to_cart(request):
    if not is_restaurant(request.user):
        from hotel_management.views import home
        return redirect(home)
        
    if request.method == 'POST':
        data = json.loads(request.body)

        item_id = data.get('item_id')
        quantity = data.get('quantity')
        reservation_id = data.get('reservation_id')

        bill, created = RestaurantBill.objects.get_or_create(reservation_id=reservation_id)

        try:
            quantity = int(quantity)
        except ValueError:
            return HttpResponse(_("The specified values aren't a valid format"), status=400)

        shoppingCart = ShoppingCart.objects.create(
            bill=bill,
            item_id=item_id,
            quantity=quantity
        )
        return HttpResponse('Instancia creada exitosamente', status=201)
    else:
        return HttpResponse('Método no permitido', status=405)


def get_available_tables(number_of_people, date, time):
    overlapping_reservations = RestaurantReservation.objects.filter(
        Q(date=date) & Q(time=time), cancelled=False
    )
    occupied_tables = [reservation.table_id for reservation in overlapping_reservations]
    all_tables = Table.objects.filter(capacity__gte=number_of_people)
    available_tables = all_tables.exclude(id__in=[table.id for table in occupied_tables])
    return available_tables


@login_required
def complete_reservation(request):
    if not is_restaurant(request.user):
        from hotel_management.views import home
        return redirect(home)
        
    data_string = request.META['QUERY_STRING']
    data = parse_qs(data_string)
    
    number_of_people = data.get('number_of_people', [''])[0]
    date = data.get('date', [''])[0]
    time = data.get('time', [''])[0]
    available_tables = get_available_tables(number_of_people, date, time)
    available_rooms = []

    if request.method == 'POST':
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
            return render(request, 'restaurant/reservation_confirmation.html', {'table_id': table.id})
    else:
        reservation_form = RestaurantReservationForm()
    return render(request, 'restaurant/add_reservation_form.html', {
                'reservation_form': reservation_form,
                'available_rooms': available_rooms,
                'available_tables': available_tables
            })