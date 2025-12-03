from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "slug", "price", "inventory_qty", "image_url", "description", "category"]
