from django.db import models

class Offer(models.Model):
    start = models.DateField()
    end = models.DateField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    ROOM_TYPE_OPTIONS = [
        ('Ind', 'Individual'),
        ('Dob', 'Doble'),
        ('Del', 'Deluxe'),
        ('Sui', 'Suite'),
        ('All', 'All')
    ]
    type = models.CharField(max_length=10, choices=ROOM_TYPE_OPTIONS)

    def __str__(self):
        return f"{self.percentage}% in {self.type}, from {self.start} to {self.end}"