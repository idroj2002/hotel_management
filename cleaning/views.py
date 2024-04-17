from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from administration.models import Room, HotelReservation

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

    return render(request, 'cleaning/cleaning_home', {'rooms_todo': sorted_rooms_todo})