from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "price",
            "inventory_qty",
            "image",       # new file upload field
            "image_url",   # optional URL fallback
            "description",
            "category",
        ]
