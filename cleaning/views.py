from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from administration.models import Room, HotelReservation
from cleaning.models import Cleaning_data
from datetime import datetime, timedelta


def is_cleaner(user):
    return user.groups.filter(name='Cleaning').exists()


def get_cleaning_data(user, room_id):
    data_list = Cleaning_data.objects.filter(room=room_id, cleaner=user, end_time=None).order_by('cleaning_day', 'starting_time')
    print(data_list)

    if data_list.count == 0:
        return None
    else:
        data = data_list.first()
        data_list.exclude(id=data.id).delete()
    return data


def was_occupied_less_than_two_hours_ago(room):
    if room.occupied:
        current_time = datetime.now()
        occupied_time = datetime.combine(current_time.date(), room.occupied)
        time_difference = current_time - occupied_time
        return time_difference < timedelta(hours=2)
    else:
        return False


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

    sorted_rooms_todo = sorted(sorted_rooms_todo, key=lambda x: was_occupied_less_than_two_hours_ago(x))
    sorted_rooms_done = sorted(sorted_rooms_done, key=lambda x: was_occupied_less_than_two_hours_ago(x))

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


@login_required
def mark_as_completed(request):
    if not is_cleaner(request.user):
        from hotel_management.views import home
        return redirect(home)
    
    room_id = request.GET.get('room_id')

    room = Room.objects.get(id=room_id)
    room.state = 'D'
    room.save()

    cleaning_data = get_cleaning_data(request.user, room_id)
    current_datetime = datetime.now()
    if cleaning_data == None:
        print("Error: Previous data not existing")

        # Create cleaning data instance
        cleaning_data = Cleaning_data.objects.create(
            cleaner=request.user,
            room_id=room_id,
            cleaning_day=current_datetime.date(),
            starting_time=current_datetime.time(),
            end_time=current_datetime.time()
        )
    else:
        cleaning_data.end_time = current_datetime.time()
        cleaning_data.save()
    return redirect(cleaning_home)


@login_required
def cancel_cleaning(request):
    if not is_cleaner(request.user):
        from hotel_management.views import home
        return redirect(home)
    
    room_id = request.GET.get('room_id')

    room = Room.objects.get(id=room_id)
    room.state = 'TD'
    room.save()

    get_cleaning_data(request.user, room_id).delete()
    return redirect(cleaning_home)


@login_required
def mark_as_occupied(request):
    if not is_cleaner(request.user):
        from hotel_management.views import home
        return redirect(home)
    
    room_id = request.GET.get('room_id')

    room = Room.objects.get(id=room_id)
    current_time = datetime.now().time()
    room.occupied = current_time
    room.save()

    return redirect(cleaning_home)
    
