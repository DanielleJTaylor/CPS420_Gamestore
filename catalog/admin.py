# catalog/admin.py
from django.contrib import admin
from .models import Product, Event, EventRegistration


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "inventory_qty", "category")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "category")
    list_filter = ("category",)


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ("user", "registered_at")
    can_delete = False


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "capacity")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "location")
    inlines = [EventRegistrationInline]


