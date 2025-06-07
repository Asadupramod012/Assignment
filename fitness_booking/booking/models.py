import uuid
from django.db import models

# Create your models here.

class Classes(models.Model):
    class_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    instructor = models.CharField(max_length=100)
    total_slots = models.IntegerField(default=10)
    available_slots = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.name}"

class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name="bookings")
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
