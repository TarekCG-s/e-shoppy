import weasyprint
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from cart.cart import Cart
from .forms import OrderCreationForm
from .models import OrderItem, Order
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
            request.session["order_id"] = order.id
            return redirect("payment:process")
    else:
        form = OrderCreationForm()
        return render(request, "orders/order/create.html", {"form": form, "cart": cart})


def export_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string(
        template_name="orders/order/pdf.html", context={"order": order}
    )
    resposne = HttpResponse(content_type="application/pdf")
    resposne["Content-Disposition"] = f'filename= "order_{order.id}'
    weasyprint.HTML(string=html).write_pdf(
        target=resposne,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + "css/pdf.css")],
    )
    return resposne
