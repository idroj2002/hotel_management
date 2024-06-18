from administration.forms import *
from django.shortcuts import render, redirect, get_object_or_404
from urllib.parse import urlencode, parse_qs
from administration.models import *
from django.db.models import QuerySet, Q
from django.contrib import messages
from clients.forms import *


def clients_home(request):
    return render(request, 'clients/clients_home.html')

def clients_profile(request):
    if request.method == 'POST':
        if ProfileClient.objects.filter(user=request.user).exists() == False:
            profile_form = ProfileClientForm(request.POST)
            if profile_form.is_valid():
                profile = profile_form.save(commit = False)
                profile.user = request.user
                profile.save()
                messages.error(request, "The profile has been saved.")
        else:
            messages.error(request, "There already exists a profile for this user.")
    profile_form = ProfileClientForm()
    return render(request, 'clients/clients_profile.html', {'profile_form':profile_form})


def clients_hotel(request):
    if request.method == 'POST' and  ProfileClient.objects.filter(user=request.user).exists():
        availability_form = AvailabilityHotelClientsCheckForm(request.POST)
        if availability_form.is_valid():
            check_in_date = availability_form.cleaned_data['check_in_date']
            check_out_date = availability_form.cleaned_data['check_out_date']
            room_type = availability_form.cleaned_data['room_type']
            room_price = get_room_price(room_type)
            number_of_guests = availability_form.cleaned_data['number_of_guests']
            data = {'check_in_date': check_in_date, 'check_out_date': check_out_date, 'room_type': room_type, 'room_price': room_price, 'number_of_guests':number_of_guests}
            complete_reservation_hotel(request, data)
            availability_form = AvailabilityHotelClientsCheckForm()
            return render(request, 'clients/clients_hotel.html',
                      {'availability_form': availability_form})
    elif request.user.is_authenticated == False:
        messages.error(request, "Please first log in and complete the profile")
        availability_form = AvailabilityHotelClientsCheckForm()
        return render(request, 'clients/clients_hotel.html',
                      {'availability_form': availability_form})
    elif ProfileClient.objects.filter(user=request.user).exists() == False:
        return redirect('clients_profile')
    else:
        availability_form = AvailabilityHotelClientsCheckForm()
        return render(request, 'clients/clients_hotel.html',
                      {'availability_form': availability_form})

def clients_restaurant(request):
    if request.method == 'POST' and  ProfileClient.objects.filter(user=request.user).exists():
        availability_form = AvailabilityRestaurantClientCheckForm(request.POST)
        if availability_form.is_valid():
            number_of_people = availability_form.cleaned_data['number_of_people']
            date = availability_form.cleaned_data['date']
            time = availability_form.cleaned_data['time']
            data = {'number_of_people': number_of_people, 'date': date, 'time': time}
            complete_reservation_restaurant(request, data)
            availability_form = AvailabilityRestaurantClientCheckForm()
            return render(request, 'clients/clients_restaurant.html',
                      {'availability_form': availability_form})
    elif request.user.is_authenticated == False:
        messages.error(request, "Please first log in and complete the profile")
        availability_form = AvailabilityRestaurantClientCheckForm()
        return render(request, 'clients/clients_restaurant.html',  {'availability_form': availability_form})
    elif ProfileClient.objects.filter(user=request.user).exists() == False:
        return redirect('clients_profile')
    else:
        availability_form = AvailabilityRestaurantClientCheckForm()
    return render(request, 'clients/clients_restaurant.html',  {'availability_form': availability_form})


def get_room_price(room_type):
    room_prices = {
        'Ind': 45,
        'Dob': 75,
        'Sui': 125,
        'Del': 100,
    }
    return room_prices.get(room_type)

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

def complete_reservation_hotel(request, data):
    profile = ProfileClient.objects.get(user=request.user)
    check_in_date = data.get('check_in_date')
    check_out_date = data.get('check_out_date')
    room_type = data.get('room_type')
    number_of_guests = data.get('number_of_guests')
    available_rooms = get_available_rooms(check_in_date, check_out_date, room_type)
    
    room = available_rooms[0]
    new_available_rooms = get_available_rooms(check_in_date, check_out_date, room_type)
    room_price = get_room_price(room.type)
    if room not in new_available_rooms:
        messages.error(request, 'There has been an error in the reservation. Try again!')
    reservation_form = HotelReservationForm()
    reservation = reservation_form.save(commit=False)
    reservation.dni = profile.dni
    reservation.first_name = profile.first_name
    reservation.last_name = profile.last_name
    reservation.date_of_birth = profile.date_of_birth
    reservation.email = profile.email
    reservation.phone = profile.phone
    reservation.number_of_guests = number_of_guests
    reservation.room_number = room
    reservation.check_in_date = check_in_date
    reservation.check_out_date = check_out_date
    reservation.price = room_price
    reservation.save()
    messages.error(request, 'Your reservation has been completed!')

def complete_reservation_restaurant(request, data):
    profile = ProfileClient.objects.get(user=request.user)
    number_of_people = data.get('number_of_people')
    date = data.get('date')
    time = data.get('time')
    available_tables = get_available_tables(number_of_people, date, time)

    table = available_tables[0]
    reservation_form = RestaurantReservationForm()
    reservation = reservation_form.save(commit=False)
    reservation.name = profile.first_name
    reservation.room_number = HotelReservation.objects.filter(dni=profile.dni).first().room_number
    reservation.table_id = table
    reservation.date = date
    reservation.number_of_people = number_of_people
    reservation.time = time
    reservation.save()
    messages.error(request, "Your reservation has been completed!")
    
def clients_reservations(request):
    profile = ProfileClient.objects.get(user=request.user)
    reservation = HotelReservation.objects.filter(dni=profile.dni).first()
    hotel_reservations = HotelReservation.objects.filter(dni=profile.dni)
    restaurant_reservations = RestaurantReservation.objects.filter(room_number=reservation.room_number)
    return render(request, 'clients/clients_reservations.html', {'hotel_reservations':hotel_reservations, 'restaurant_reservations':restaurant_reservations})
