from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Room(models.Model):
    number = models.IntegerField()
    type = models.CharField(max_length=100)
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Room {self.number}"


class Table(models.Model):
    id = models.AutoField(primary_key=True)
    capacity = models.IntegerField()
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Table {self.id}"


class HotelReservation(models.Model):
    id = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
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

    def __str__(self):
        return f"Reservation for {self.first_name} {self.last_name}"


class RestaurantReservation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    room_number = models.IntegerField(blank=True, null=True)
    number_of_people = models.IntegerField()
    table_id = models.ForeignKey(Table, on_delete=models.CASCADE)
    time = models.DateTimeField()

    def __str__(self):
        return f"Restaurant reservation for {self.name}"
