import csv
from django.http import HttpResponse
from django.shortcuts import reverse
from django.contrib import admin
from django.utils.html import mark_safe
from .models import Order, OrderItem


def export_order_pdf(obj):
    return mark_safe(
        '<a href="{}">PDF</a>'.format(
            reverse("orders:export_order_pdf", kwargs={"order_id": obj.id})
        )
    )


export_order_pdf.short_description = "Invoice"


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename={}.csv".format(
        opts.verbose_name
    )
    writer = csv.writer(response)

    headers = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    writer.writerow([header.verbose_name for header in headers])
    for obj in queryset:
        row = []
        for field in headers:
            val = getattr(obj, field.name)
            row.append(val)
        writer.writerow(row)
    return response


export_to_csv.short_description = "Export To CSV"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "address",
        "postal_code",
        "city",
        "paid",
        "created",
        "updated",
        export_order_pdf,
    ]

    actions = [export_to_csv]
    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]
