# catalog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # PRODUCTS
    path("", views.product_list, name="product_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("product/create/", views.product_create, name="product_create"),
    path("product/<slug:slug>/edit/", views.product_edit, name="product_edit"),

    # CART
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("cart/update/<int:product_id>/", views.cart_update_quantity, name="cart_update"),
    path("cart/clear/", views.cart_clear, name="cart_clear"),

    # EVENTS
    path("events/", views.event_list, name="event_list"),
    path("events/create/", views.event_create, name="event_create"),
    path("events/<slug:slug>/", views.event_detail, name="event_detail"),
    path("events/<slug:slug>/register/", views.event_register, name="event_register"),
    path("events/<slug:slug>/unregister/", views.event_unregister, name="event_unregister"),

    # ROOMS / ROOM BOOKINGS
    path("rooms/", views.room_booking_list, name="room_booking_list"),
    path("rooms/<slug:slug>/book/", views.room_booking_create, name="room_booking_create"),
    path(
        "rooms/bookings/<int:booking_id>/cancel/",
        views.room_booking_cancel,
        name="room_booking_cancel",
    ),
]
