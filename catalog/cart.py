# catalog/cart.py
from decimal import Decimal
from django.conf import settings
from .models import Product

CART_SESSION_ID = "cart"

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if cart is None:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        # Don't allow quantity to go below 1 here
        if self.cart[product_id]["quantity"] < 1:
            self.remove(product)
        else:
            self.save()

    def decrement(self, product, quantity=1):
        """
        Decrease quantity; if it hits 0, remove the product.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] -= quantity
            if self.cart[product_id]["quantity"] <= 0:
                self.remove(product)
            else:
                self.save()

    def remove(self, product):
        """
        Remove a product entirely from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        """
        Remove cart from session.
        """
        if CART_SESSION_ID in self.session:
            del self.session[CART_SESSION_ID]
            self.session.modified = True

    def __iter__(self):
        """
        Iterate over cart items with Product objects and total_price.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            item = cart[str(product.id)]
            item["product"] = product
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Total quantity of items.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )
