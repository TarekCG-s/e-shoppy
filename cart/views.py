from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartCreationForm
from coupons.forms import CouponApplyForm


@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartCreationForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data["quantity"]
        cart.add_item(product, quantity=quantity)
    return redirect("cart:cart_detail")


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_item(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm()
    for item in cart:
        item["update_form"] = CartCreationForm(initial={"quantity": item["quantity"]})
    return render(
        request,
        "cart/detail.html",
        {"cart": cart, "coupon_apply_form": coupon_apply_form},
    )
