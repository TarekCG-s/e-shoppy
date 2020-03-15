from django.shortcuts import render
from django.shortcuts import get_object_or_404
from cart.forms import CartCreationForm
from .models import Category, Product


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    category = None
    products = Product.objects.all()
    if category_slug:

        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    context = {"category": category, "categories": categories, "products": products}
    return render(request, "shop/product/list.html", context=context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    form = CartCreationForm()
    return render(
        request, "shop/product/detail.html", {"product": product, "form": form}
    )
