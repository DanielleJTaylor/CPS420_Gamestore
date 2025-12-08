from django import forms
from .models import Product, Event, RoomBooking, Room


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


class RoomBookingForm(forms.ModelForm):
    class Meta:
        model = RoomBooking
        fields = ["room", "date", "start_time", "end_time"]

        widgets = {
            "room": forms.Select(),
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean(self):
        cleaned = super().clean()
        room = cleaned.get("room")
        date = cleaned.get("date")
        start = cleaned.get("start_time")
        end = cleaned.get("end_time")

        if start and end and start >= end:
            raise forms.ValidationError("End time must be after start time.")

        # basic overlap check (view will also enforce)
        if room and date and start and end:
            qs = RoomBooking.objects.filter(
                room=room,
                date=date,
                start_time__lt=end,
                end_time__gt=start,
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("This time slot is already booked.")

        return cleaned
