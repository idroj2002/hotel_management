from django.utils import timezone
from datetime import timedelta
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
    state = models.CharField(max_length=10, choices=ROOM_STATE_OPTIONS, default='TD')
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
    number_of_nights = models.IntegerField(default=1)
    number_of_guests = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    ROOM_TYPE_OPTIONS = [
        ('Ind', 'Individual'),
        ('Dob', 'Doble'),
        ('Del', 'Deluxe'),
        ('Sui', 'Suite'),
    ]
    room_type = models.CharField(max_length=100, choices=ROOM_TYPE_OPTIONS, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
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
    date = models.DateField(default=timezone.now)
    TURN_CHOICES = [
        ('breakfast_1', 'Desayuno - Primer Turno'),
        ('breakfast_2', 'Desayuno - Segundo Turno'),
        ('lunch_1', 'Comida - Primer Turno'),
        ('lunch_2', 'Comida - Segundo Turno'),
        ('dinner_1', 'Cena - Primer Turno'),
        ('dinner_2', 'Cena - Segundo Turno'),
    ]

    time = models.CharField(choices=TURN_CHOICES, max_length=20)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        # formatted_time = self.time.strftime('%d/%m %H:%M')
        return f"ID: {self.id} - Nombre: {self.name} - Fecha: {self.date} - Turno: {self.time}"


class CheckIn(models.Model):
    id = models.OneToOneField(HotelReservation, on_delete=models.CASCADE, primary_key=True)
    guests_data = models.TextField(max_length=1000)
    number_of_guests = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    number_of_nights = models.PositiveIntegerField(default=0)
    keys = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    cancelled = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.number_of_nights = self.id.number_of_nights
        self.number_of_guests = self.id.number_of_guests
        super().save(*args, **kwargs)

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
