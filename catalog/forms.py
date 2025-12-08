from django import forms
from .models import Product, Event


class ProductForm(forms.ModelForm):
    """
    Form used by staff/admin to create or edit products.
    Supports uploaded images and optional external image URLs.
    """

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
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "inventory_qty": forms.NumberInput(
                attrs={"class": "form-control", "min": "0"}
            ),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "image_url": forms.URLInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "category": forms.TextInput(attrs={"class": "form-control"}),
        }


class EventForm(forms.ModelForm):
    """
    Staff-only form to create or edit events that customers can register for.
    """

    class Meta:
        model = Event
        fields = ["title", "slug", "description", "start_time", "capacity"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "start_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "capacity": forms.NumberInput(
                attrs={"class": "form-control", "min": "0"}
            ),
        }
