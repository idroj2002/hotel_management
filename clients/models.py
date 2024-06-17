from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProfileClient(models.Model):
    id = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"ID: {self.id} - Nombre: {self.first_name} {self.last_name}"