from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from .models import Product
from .forms import ProductForm


def product_list(request):
    """
    Show all products on the homepage.
    """
    products = Product.objects.all().order_by("-id")
    return render(request, "catalog/product_list.html", {"products": products})


def product_detail(request, slug):
    """
    Show a single product detail page by slug.
    """
    product = get_object_or_404(Product, slug=slug)
    return render(request, "catalog/product_detail.html", {"product": product})


def is_staff_user(user):
    """
    Helper used by user_passes_test to allow only staff/admin users.
    """
    return user.is_staff


@user_passes_test(is_staff_user)
def product_create(request):
    """
    Create a new product.
    Only staff/admin users can access this view.
    Supports image uploads via ProductForm.
    """
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect("product_detail", slug=product.slug)
    else:
        form = ProductForm()

    return render(request, "catalog/product_form.html", {"form": form})


def signup(request):
    """
    Simple user registration.
    Creates a new user and logs them in immediately.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("product_list")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


def logout_view(request):
    """
    Log the current user out and redirect to product list.
    Allows GET so the navbar link works without 405 errors.
    """
    logout(request)
    return redirect("product_list")
