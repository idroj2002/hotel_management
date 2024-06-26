from django.contrib import admin
from administration.models import Room, Table, HotelReservation, RestaurantReservation, CheckIn, CheckOut
from cleaning.models import Cleaning_data
from accounting.models import Offer


# Custom admin classes
class RoomAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


class TableAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


# Register your models here.
admin.site.register(Room)
admin.site.register(Table, TableAdmin)
admin.site.register(HotelReservation)
admin.site.register(RestaurantReservation)
admin.site.register(CheckIn)
admin.site.register(CheckOut)

admin.site.register(Cleaning_data)

admin.site.register(Offer)
