from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "inventory_qty", "category")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "category")
    list_filter = ("category",)
