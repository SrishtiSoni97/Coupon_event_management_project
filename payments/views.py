import stripe
import time

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import transaction
from django.utils.timezone import now
from django.contrib import messages

from events.models import Event
from orders.models import Order
from tickets.models import Ticket
from payments.models import Payment
from tickets.utils import generate_qr_code

# Stripe secret key
stripe.api_key = settings.STRIPE_SECRET_KEY


# ============================
# PAYMENT PAGE
# ============================
@login_required
def payment_page(request):
    data = request.session.get("checkout_data")

    if not data:
        messages.error(request, "Session expired. Please checkout again.")
        return redirect("checkout")

    event = get_object_or_404(Event, id=data["event_id"])

    return render(request, "user/payment.html", {
        "event": event,
        "qty": data["qty"],
        "total_amount": data["total"],
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "show_hero": False
    })


# ============================
# CREATE STRIPE CHECKOUT SESSION
# 
# ============================
@login_required
def create_stripe_session(request):
    data = request.session.get("checkout_data")

    if not data:
        return redirect("checkout")

    event = get_object_or_404(Event, id=data["event_id"])
    qty = int(data["qty"])

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "inr",
                "product_data": {"name": event.title},
                "unit_amount": int(event.price * 100),
            },
            "quantity": qty,
        }],
        success_url=request.build_absolute_uri("/payment/success/"),
        cancel_url=request.build_absolute_uri("/payment/fail/"),
        metadata={
            "user_id": request.user.id,
            "event_id": event.id,
            "quantity": qty,
        }
    )

    return redirect(session.url)


# ============================
# SUCCESS PAGE (DISPLAY ONLY)
# ============================
@login_required
def payment_success(request):
    #  CLEAR CART + CHECKOUT DATA
    request.session.pop("cart", None)
    request.session.pop("checkout_data", None)
    request.session.modified = True

    order = (
        Order.objects
        .filter(user=request.user, order_status="PAID")
        .order_by("-id")
        .first()
    )

    if not order:
        messages.error(request, "Order not found.")
        return redirect("home")

    return render(request, "user/order-success.html", {
        "order": order,
        "show_hero": False
    })




# ============================
# STRIPE WEBHOOK 
# ============================
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        user_id = session["metadata"]["user_id"]
        event_id = session["metadata"]["event_id"]
        qty = int(session["metadata"]["quantity"])
        payment_intent = session["payment_intent"]

        with transaction.atomic():
            event_db = Event.objects.select_for_update().get(id=event_id)

            if event_db.available_coupons < qty:
                return HttpResponse(status=400)

            order = Order.objects.create(
                user_id=user_id,
                event=event_db,
                quantity=qty,
                total_amount=event_db.price * qty,
                order_status="PAID",
                order_code=f"ORD-{int(time.time())}"
            )

            Payment.objects.create(
                order=order,
                payment_gateway="STRIPE",
                transaction_id=payment_intent,
                payment_method="CARD",
                amount=order.total_amount,
                payment_status="SUCCESS",
                paid_at=now()
            )

            #  CORRECT TICKET + QR CREATION
            for i in range(qty):
                ticket = Ticket.objects.create(
                    order=order,
                    ticket_code=f"TCK-{order.id}-{i}"
                )
                generate_qr_code(ticket)

            event_db.available_coupons -= qty
            event_db.save()

    return HttpResponse(status=200)


# ============================
# PAYMENT FAILED / CANCELLED
# ============================
@login_required
def payment_fail(request):
    # Clean checkout session data
    request.session.pop("checkout_data", None)

    messages.error(
        request,
        "Payment failed or was cancelled. Please try again."
    )

    return render(request, "user/payment-fail.html", {
        "show_hero": False
    })
