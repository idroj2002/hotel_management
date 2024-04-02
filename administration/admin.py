from django.contrib import admin
from administration.models import Room, Table, HotelReservation, RestaurantReservation


# Custom admin classes
class RoomAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


class TableAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


# Register your models here.
admin.site.register(Room, RoomAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(HotelReservation)
admin.site.register(RestaurantReservation)
