import braintree
import weasyprint
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from orders.models import Order


def process_payment(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        nonce = request.POST.get("payment_method_nonce", None)
        result = braintree.Transaction.sale(
            {
                "amount": "{:.2f}".format(order.get_total_cost()),
                "payment_method_nonce": nonce,
                "options": {"submit_for_settlement": True},
            }
        )
        if result.is_success:
            order.paid = True
            order.transaction_id = result.transaction.id
            order.save()
            subject = f"E-Shoppy - Order {order.id} - Invoice"
            body = f"you have successfuly paid {order.id}. please check the attached file below."
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email="no-reply@e-shoppy.com",
                to=[order.email],
            )
            io = BytesIO()
            html = render_to_string("orders/order/pdf.html", context={"order": order})
            weasyprint.HTML(string=html).write_pdf(
                io, stylesheets=[settings.STATIC_ROOT + "css/pdf.css"]
            )
            email.attach(
                f"invoice_order_{order.id}.pdf",
                io.getvalue(),
                mimetype="application/pdf",
            )
            email.send()
            return redirect("payment:success")
        else:
            return redirect("payment:cancel")

    else:
        client_token = braintree.ClientToken.generate()
        return render(
            request,
            "payment/process.html",
            context={"order": order, "client_token": client_token},
        )


def payment_success(request):
    return render(request, "payment/success.html")


def payment_cancel(request):
    return render(request, "payment/cancel.html")
