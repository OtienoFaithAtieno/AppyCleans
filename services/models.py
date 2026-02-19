# services/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        null=False,
        blank=False
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("confirmed", "Confirmed"),("completed", "Completed"),  ("cancelled", "Cancelled"),], default="pending")
   
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['service', 'date', 'time'],
                name='unique_service_booking'
            )
        ]
   
    def __str__(self):
        return f"{self.user.username} - {self.service.name} on ({self.date})"
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    
class LaundryPickup(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("picked_up", "Picked Up"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='laundry_pickups'
    )

    address = models.TextField()
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    special_instructions = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Pickup ({self.pickup_date})"


class DeliveryRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("out_for_delivery", "Out for Delivery"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='deliveries'
    )

    pickup_address = models.TextField()
    delivery_address = models.TextField()
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    notes = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Delivery ({self.delivery_date})"

