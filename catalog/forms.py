# catalog/forms.py
from django import forms
from django.utils.text import slugify
from django.utils import timezone

from .models import Product, Event, RoomBooking


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "price",
            "inventory_qty",
            "image",
            "image_url",
            "description",
            "category",
        ]

    def clean_slug(self):
        """
        If slug is blank, auto-generate it from the name.
        """
        slug = self.cleaned_data.get("slug")
        name = self.cleaned_data.get("name")

        if not slug and name:
            slug = slugify(name)

        return slug


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "slug",
            "description",
            "date",
            "start_time",
            "capacity",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        title = self.cleaned_data.get("title")
        if not slug and title:
            slug = slugify(title)
        return slug


class RoomBookingForm(forms.ModelForm):
    """
    Form for booking a room.

    We expose:
    - room: which room to book
    - start_time, end_time: when the booking runs
    """

    class Meta:
        model = RoomBooking
        fields = [
            "room",
            "start_time",
            "end_time",
        ]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean(self):
        """
        Basic validation:
        - end_time must be after start_time
        - start_time must not be in the past
        """
        cleaned = super().clean()
        start = cleaned.get("start_time")
        end = cleaned.get("end_time")

        if start and end and end <= start:
            self.add_error("end_time", "End time must be after start time.")

        if start and start < timezone.now():
            self.add_error("start_time", "Start time cannot be in the past.")

        return cleaned
