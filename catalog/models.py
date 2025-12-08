from django.db import models
from django.conf import settings
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_qty = models.PositiveIntegerField(default=0)

    # Uploaded image from computer (stored in /media/product_images/)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)

    # Optional: external image URL as a fallback
    image_url = models.URLField(blank=True)

    description = models.TextField(blank=True)
    category = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    description = models.TextField(blank=True)

    # explicit calendar date for the event
    date = models.DateField(default=timezone.now)

    # full datetime for when it starts
    start_time = models.DateTimeField(default=timezone.now)

    capacity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "start_time"]

    def __str__(self):
        return self.title

    @property
    def registrations_count(self):
        return self.registrations.count()

    @property
    def remaining_spots(self):
        if self.capacity == 0:
            return None  # unlimited
        return max(self.capacity - self.registrations_count, 0)


class EventRegistration(models.Model):
    event = models.ForeignKey(
        Event,
        related_name="registrations",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "user")
        ordering = ["-registered_at"]

    def __str__(self):
        return f"{self.user} -> {self.event}"


# =========================
# ROOM BOOKING
# =========================

class Room(models.Model):
    """
    Fixed set of rooms in the store.
    """
    name = models.CharField(max_length=100, unique=True)
    # hex color used for calendar tag
    color = models.CharField(max_length=7, default="#2563eb")

    def __str__(self):
        return self.name


class RoomBooking(models.Model):
    """
    A single room reservation on a given date/time by a user.
    """
    ROOM_CHOICES = (
        ("Large TTRPG", "Large TTRPG"),
        ("Small Private TTRPG", "Small Private TTRPG"),
        ("TV Lounge", "TV Lounge"),
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    date = models.DateField()  # calendar date
    start_time = models.TimeField()
    end_time = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.room.name} on {self.date} ({self.start_time}-{self.end_time})"

    @property
    def label(self):
        return f"{self.date} {self.start_time}-{self.end_time}"
