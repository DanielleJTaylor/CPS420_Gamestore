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


from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product, quantity=1)
    return redirect("cart_detail")


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart_detail")


def cart_update(request, product_id):
    """
    Adjust quantity using up/down buttons.
    direction = 'up' → +1
    direction = 'down' → -1
    If qty falls to 0 or below, item is removed.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        direction = request.POST.get("direction")
        # current quantity in the cart
        current_qty = cart.cart.get(str(product.id), {}).get("quantity", 0)

        if direction == "up":
            qty = current_qty + 1
        elif direction == "down":
            qty = current_qty - 1
        else:
            # fallback: numeric quantity if ever needed
            try:
                qty = int(request.POST.get("quantity", current_qty))
            except ValueError:
                qty = current_qty

        # clamp and update
        qty = max(0, min(qty, 999))
        cart.add(product, quantity=qty, override_quantity=True)

    return redirect("cart_detail")





signup_view = signup