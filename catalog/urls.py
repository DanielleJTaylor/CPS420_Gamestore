from django.urls import path
from . import views

urlpatterns = [
    # Homepage – product list
    path("", views.product_list, name="product_list"),

    # Create new product (must come BEFORE the slug route)
    path("product/new/", views.product_create, name="product_create"),

    # Product detail by slug
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),

    # User signup
    path("signup/", views.signup, name="signup"),
]
