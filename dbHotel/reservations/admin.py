from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    exclude = ['user']
    list_display = (
        'id', 'user','room_id', 'room_name','room_price', 'check_in', 'check_out',
        'adults', 'children', 'get_room_numbers',
        'total_amount', 'payment_method', 'date_reserved'
    )

    def room_name(self, obj):
        # Assuming room is a related model, modify as per your actual relationship
        return obj.room.name  # Adjust based on how you've linked the Room model
    room_name.short_description = 'Room Name'

    def get_room_numbers(self, obj):
       return ", ".join(str(room) for room in obj.room_numbers or [])


    get_room_numbers.short_description = 'Room Numbers'
