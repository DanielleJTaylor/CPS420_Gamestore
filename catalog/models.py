from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_qty = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.name
