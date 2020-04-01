from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.create_order, name="create_order"),
    path(
        "admin/order/<int:order_id>/pdf/",
        views.export_order_pdf,
        name="export_order_pdf",
    ),
]
