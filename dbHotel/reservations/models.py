from django.db import models
from django.contrib.auth.models import User
from rooms.models import Room  # Import Room from rooms app

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    room_id = models.IntegerField(default=1, null=True, blank=True)  # Room ID (default 1 if not provided)
    room_name = models.CharField(max_length=100)  # Name of the room
    room_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the room
    adults = models.IntegerField()
    children = models.IntegerField()
    room_numbers = models.JSONField()  # Stores room numbers
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total reservation cost
    payment_method = models.CharField(max_length=50)  # Payment method (GCASH, VISA, etc.)
    date_reserved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation for {self.room_name} from {self.check_in} to {self.check_out}"
