from django.db import models
from administration.models import RestaurantReservation

class RestaurantItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(blank=True, null=True)

class RestaurantBill(models.Model):
    id = models.AutoField(primary_key=True)
    reservation = models.ForeignKey(RestaurantReservation, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)

    def __str__(self):
        cart_items = self.shoppingcart_set.all()
        total = sum(item.item.price * item.quantity for item in cart_items)

        return f"ID: {self.id}, Date: {self.reservation.date}, Quantity: {total}"
    
class ShoppingCart(models.Model):
    id = models.AutoField(primary_key=True)
    bill = models.ForeignKey(RestaurantBill, on_delete=models.CASCADE)
    item = models.ForeignKey(RestaurantItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

