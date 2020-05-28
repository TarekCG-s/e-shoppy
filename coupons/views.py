from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .forms import CouponApplyForm
from .models import Coupon


@require_POST
def apply_coupon(request):
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data.get("coupon")
        now = timezone.now()
        coupon = Coupon.objects.filter(
            code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True
        ).last()
        print(coupon)
    if coupon:
        request.session["coupon_id"] = coupon.id
    return redirect("cart:cart_detail")
