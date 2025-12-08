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

    # full datetime (you can later change to TimeField if you want only time)
    start_time = models.DateTimeField(default=timezone.now)

    capacity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # sort upcoming events by date, then time
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
# ROOMS & ROOM BOOKINGS
# =========================

class Room(models.Model):
    """
    A physical gaming room (Small TTRPG, Large TTRPG, TV Lounge).
    """

    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    # how many players can fit comfortably
    capacity = models.PositiveIntegerField(default=4)

    # short blurb for the UI
    description = models.TextField(blank=True)

    # optional color for UI (e.g., calendar tag)
    color = models.CharField(max_length=7, default="#2563eb")  # hex like "#2563eb"

    def __str__(self):
        return self.name


class RoomBooking(models.Model):
    """
    A single reservation of a room by a user.
    Tracks start/end time and an optional fee.
    """

    room = models.ForeignKey(
        Room,
        related_name="bookings",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # simple money field; you can ignore if you don't care right now
    fee_charged = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.room.name} for {self.user} at {self.start_time}"
