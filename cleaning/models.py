from django.db import models
from django.conf import settings
from administration.models import Room

USER = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Cleaning_data(models.Model):
    cleaner = models.ForeignKey(USER, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    cleaning_day = models.DateField()
    starting_time = models.TimeField()
    end_time = models.TimeField(null=True)