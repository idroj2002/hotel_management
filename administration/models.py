from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Room(models.Model):
    number = models.IntegerField()
    ROOM_TYPE_OPTIONS = [
            ('Ind', 'Individual'),
            ('Dob', 'Doble'),
            ('Del', 'Deluxe'),
            ('Sui', 'Suite'),
        ]
    type = models.CharField(max_length=100, choices=ROOM_TYPE_OPTIONS)
    ROOM_STATE_OPTIONS = [
        ('TD', 'To-do'),
        ('P', 'In process'),
        ('D', 'Done'),
    ]
    state = models.CharField(max_length=10, choices=ROOM_STATE_OPTIONS)
    occupied = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Habitación {self.number} ({self.type})"


class Table(models.Model):
    id = models.AutoField(primary_key=True)
    capacity = models.IntegerField()
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Mesa {self.id} ({self.capacity} people)"


class HotelReservation(models.Model):
    id = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    ROOM_TYPE_OPTIONS = [
            ('Ind', 'Individual'),
            ('Dob', 'Doble'),
            ('Del', 'Deluxe'),
            ('Sui', 'Suite'),
        ]
    room_type = models.CharField(max_length=100, choices=ROOM_TYPE_OPTIONS, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"ID: {self.id} - Nombre: {self.first_name} {self.last_name} - Entrada: {self.check_in_date}" \
               f" - Saldia: {self.check_out_date}"


class RestaurantReservation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    number_of_people = models.IntegerField()
    table_id = models.ForeignKey(Table, on_delete=models.CASCADE)
    time = models.DateTimeField()
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        formatted_time = self.time.strftime('%d/%m %H:%M')
        return f"ID: {self.id} - Nombre: {self.name} - Hora: {formatted_time}"


class CheckIn(models.Model):
    id = models.OneToOneField(HotelReservation, on_delete=models.CASCADE, primary_key=True)
    guests_data = models.TextField(max_length=1000)
    keys = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"Check-In    of reservation: {self.id}"


class CheckOut(models.Model):
    id = models.OneToOneField(HotelReservation, on_delete=models.CASCADE, primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    keys = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"Check-Out of reservation: {self.id}"
