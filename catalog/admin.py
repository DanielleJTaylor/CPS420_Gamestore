from django.contrib import admin
from .models import Product, Event, EventRegistration


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "inventory_qty", "category")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "category")
    list_filter = ("category",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_time", "capacity")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "registered_at")
    list_filter = ("event", "registered_at")

