from django.shortcuts import render
from cart.cart import Cart
from .forms import OrderCreationForm
from .models import OrderItem
from .tasks import send_email


def create_order(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            subject = f"Order {order.id} has been placed"
            message = f"Dear {order.first_name}, you have successfully placed order {order.id}"
            emails = [order.email]
            send_email.delay(subject, message, emails)
            return render(
                request, "orders/order/created.html", context={"order": order}
            )
    else:
        form = OrderCreationForm()
        return render(request, "orders/order/create.html", {"form": form, "cart": cart})
