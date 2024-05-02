from django.contrib import admin
from restaurant.models import RestaurantItem, RestaurantBill, ShoppingCart

admin.site.register(RestaurantItem)
admin.site.register(RestaurantBill)
admin.site.register(ShoppingCart)