from django.db import models

class Room(models.Model):
    room_number = models.IntegerField(unique=True)
    room_name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=100)
    room_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='available')  # <-- Added field for availability status

    def __str__(self):
        return f"Room {self.room_number} ({self.room_name})"

