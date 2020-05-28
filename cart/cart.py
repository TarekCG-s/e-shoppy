from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from shop.models import Product
from coupons.models import Coupon


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = request.session.get("coupon_id", None)

    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        coupon = self.coupon()
        if coupon:
            return coupon.discount / Decimal("100") * self.get_total_price()
        return Decimal("0")

    def get_discounted_total_price(self):
        return self.get_total_price() - self.get_discount()

    def add_item(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
                "name": product.name,
            }
        self.cart[product_id]["quantity"] = quantity
        self.save()

    def remove_item(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        return sum(
            item["quantity"] * Decimal(item["price"]) for item in self.cart.values()
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]

    def __iter__(self):
        cart = self.cart.copy()
        keys = cart.keys()
        for key in keys:
            product = get_object_or_404(Product, id=key)
            if product:
                cart[key]["product"] = product
            cart[key]["total_price"] = (
                Decimal(cart[key]["price"]) * cart[key]["quantity"]
            )
            yield cart[key]

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())
