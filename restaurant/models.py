from django.db import models
from administration.models import RestaurantReservation

class RestaurantItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)

class RestaurantBill(models.Model):
    id = models.AutoField(primary_key=True)
    reservation = models.ForeignKey(RestaurantReservation, on_delete=models.CASCADE)
    
class ShoppingCart(models.Model):
    id = models.AutoField(primary_key=True)
    bill = models.ForeignKey(RestaurantBill, on_delete=models.CASCADE)
    item = models.ForeignKey(RestaurantItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

