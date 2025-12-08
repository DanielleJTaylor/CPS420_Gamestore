from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages

from .models import Product, Event, EventRegistration
from .forms import ProductForm, EventForm
from .cart import Cart


# =========================
# HELPERS
# =========================

def is_staff_user(user):
    """
    Helper used by user_passes_test to allow only staff/admin users.
    """
    return user.is_staff


# =========================
# PRODUCT VIEWS
# =========================

def product_list(request):
    """
    Show all products on the homepage.
    Optional search by ?q=.
    """
    products = Product.objects.all().order_by("-id")

    query = request.GET.get("q")
    if query:
        products = products.filter(name__icontains=query)

    return render(request, "catalog/product_list.html", {"products": products})


def product_detail(request, slug):
    """
    Show a single product detail page by slug.
    """
    product = get_object_or_404(Product, slug=slug)
    return render(request, "catalog/product_detail.html", {"product": product})


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
            messages.success(request, "Product created successfully.")
            return redirect("product_detail", slug=product.slug)
    else:
        form = ProductForm()

    return render(request, "catalog/product_form.html", {"form": form})


@user_passes_test(is_staff_user)
def product_edit(request, slug):
    """
    Edit an existing product (staff only).
    """
    product = get_object_or_404(Product, slug=slug)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("product_detail", slug=product.slug)
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "catalog/product_form.html",
        {"form": form, "edit_mode": True, "product": product},
    )


# =========================
# AUTH VIEWS (SIGNUP / LOGOUT)
# =========================

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
            messages.success(request, "Account created – you’re now logged in!")
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


# Alias used in urls.py from earlier instructions
signup_view = signup


# =========================
# CART VIEWS
# =========================

def cart_detail(request):
    """
    Show the current cart.
    """
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


def cart_add(request, product_id):
    """
    Add a product to the cart (default quantity 1).
    Typically called via POST from the product list/detail.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product, quantity=1)
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect("cart_detail")


def cart_remove(request, product_id):
    """
    Remove a product entirely from the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f"Removed {product.name} from your cart.")
    return redirect("cart_detail")


def cart_update_quantity(request, product_id):
    """
    Adjust quantity using up/down arrow buttons.

    Expects a POST with a hidden "action" field:
      - action="inc" → increment by 1
      - action="dec" → decrement by 1 (and remove if it hits 0)
    """
    if request.method != "POST":
        return redirect("cart_detail")

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    action = request.POST.get("action")

    if action == "inc":
        # increase quantity by 1
        cart.add(product, quantity=1)
    elif action == "dec":
        # decrease quantity by 1 – relies on Cart.add() handling <=0 as remove
        cart.add(product, quantity=-1)

    return redirect("cart_detail")


def cart_clear(request):
    """
    Optional: clear the entire cart.
    """
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Cart cleared.")
    return redirect("cart_detail")


# =========================
# EVENT VIEWS
# =========================

def event_list(request):
    """
    List all upcoming events that customers can register for.
    """
    events = Event.objects.all().order_by("start_time")
    return render(request, "events/event_list.html", {"events": events})


def event_detail(request, slug):
    """
    Show a single event with registration info.
    """
    event = get_object_or_404(Event, slug=slug)
    is_registered = False

    if request.user.is_authenticated:
        is_registered = EventRegistration.objects.filter(
            event=event, user=request.user
        ).exists()

    current_count = EventRegistration.objects.filter(event=event).count()

    context = {
        "event": event,
        "is_registered": is_registered,
        "current_count": current_count,
    }
    return render(request, "events/event_detail.html", context)


@user_passes_test(is_staff_user)
def event_create(request):
    """
    Staff-only: create a new event.
    """
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, "Event created successfully.")
            return redirect("event_detail", slug=event.slug)
    else:
        form = EventForm()

    return render(request, "events/event_form.html", {"form": form})


@login_required
def event_register(request, slug):
    """
    Customer: register for an event if:
      - capacity not full
      - not already registered
    """
    event = get_object_or_404(Event, slug=slug)

    # Check if already registered
    if EventRegistration.objects.filter(event=event, user=request.user).exists():
        messages.info(request, "You are already registered for this event.")
        return redirect("event_detail", slug=event.slug)

    # Capacity check
    current_count = EventRegistration.objects.filter(event=event).count()
    if event.capacity is not None and current_count >= event.capacity:
        messages.error(request, "This event is full.")
        return redirect("event_detail", slug=event.slug)

    # Create registration
    EventRegistration.objects.create(event=event, user=request.user)
    messages.success(request, "You are registered for this event!")
    return redirect("event_detail", slug=event.slug)


@login_required
def event_unregister(request, slug):
    """
    Optional: allow a user to unregister from an event.
    """
    event = get_object_or_404(Event, slug=slug)
    EventRegistration.objects.filter(event=event, user=request.user).delete()
    messages.info(request, "You have been unregistered from this event.")
    return redirect("event_detail", slug=event.slug)
