from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm

def product_list(request):
    products = Product.objects.all().order_by("-id")
    return render(request, "catalog/product_list.html", {"products": products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "catalog/product_detail.html", {"product": product})

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect("product_detail", slug=product.slug)
    else:
        form = ProductForm()
    return render(request, "catalog/product_form.html", {"form": form})
