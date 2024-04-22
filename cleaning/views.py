from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from administration.models import Room, HotelReservation
from cleaning.models import Cleaning_data
from datetime import datetime

# Create your views here.

def is_cleaner(user):
    return user.groups.filter(name='Cleaning').exists()


@login_required
def cleaning_home(request):
    if not is_cleaner(request.user):
        from hotel_management.views import home
        return redirect(home)
    
    reservations = HotelReservation.objects.all()
    rooms = Room.objects.all()

    # Get the reservetions relatad to today
    current_date = timezone.now().date()
    reservations = HotelReservation.objects.filter(check_in_date__gte=current_date)

    # Sort rooms by priority (more priority if exist a check-in)
    rooms_with_reservation = []
    rooms_without_reservation = []
    for room in rooms:
        if reservations.filter(room_number=room).exists():
            rooms_with_reservation.append(room)
        else:
            rooms_without_reservation.append(room)
    
    sorted_rooms = sorted(rooms_with_reservation, key=lambda x: x.number) + sorted(rooms_without_reservation, key=lambda x: x.number)
    sorted_rooms_todo = [room for room in sorted_rooms if(room.state != 'D')]
    sorted_rooms_done = [room for room in sorted_rooms if(room.state == 'D')]

    # Search recommended room
    recommended_room = None
    for room in sorted_rooms_todo:
        if room.state == 'TD':
            recommended_room = room
            break

    return render(request, 'cleaning/cleaning_home.html',
    {
        'rooms_todo': sorted_rooms_todo, 
        'recommended_room': recommended_room,
        'rooms_done': sorted_rooms_done
    })

@login_required
def create_cleaning_data(request):
    if not is_cleaner(request.user):
        from hotel_management.views import home
        return redirect(home)

    current_datetime = datetime.now()

    room_id = request.GET.get('room_id')
    cleaning_day = current_datetime.date()
    starting_time = current_datetime.time()
    end_time = None

    # Set cleaner as the authenticated user
    cleaner = request.user

    # Create cleaning data instance
    cleaning_data = Cleaning_data.objects.create(
        cleaner=cleaner,
        room_id=room_id,
        cleaning_day=cleaning_day,
        starting_time=starting_time,
        end_time=end_time
    )

    # Set new room state
    room = Room.objects.get(id=room_id)
    room.state = 'P'
    room.save()

    return redirect(cleaning_home)