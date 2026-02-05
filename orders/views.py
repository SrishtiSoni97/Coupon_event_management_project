from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now

from events.models import Event
from .models import Order


# ==================================================
# CART HELPERS
# ==================================================

def get_cart(request):
    return request.session.get("cart", {})


def save_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True


# ==================================================
# ADD TO CART
# ==================================================

@login_required
def add_to_cart(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    #  Block expired events
    if event.event_ticket_last_purchase_date < now().date():
        messages.error(request, "Ticket sales for this event have expired.")
        return redirect("user_dashboard")

    #  Block sold-out events
    if event.available_coupons <= 0:
        messages.error(request, "Tickets are sold out.")
        return redirect("user_dashboard")

    cart = get_cart(request)
    current_qty = cart.get(str(event_id), 0)

    #  Block exceeding availability
    if current_qty + 1 > event.available_coupons:
        messages.error(request, "Not enough tickets available.")
        return redirect("cart")

    cart[str(event_id)] = current_qty + 1
    save_cart(request, cart)

    messages.success(request, "Ticket added to cart.")
    return redirect("cart")


# ==================================================
# BUY NOW
# ==================================================

@login_required
def buy_now(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.event_ticket_last_purchase_date < now().date():
        messages.error(request, "Ticket sales have expired.")
        return redirect("user_dashboard")

    if event.available_coupons <= 0:
        messages.error(request, "Tickets are sold out.")
        return redirect("user_dashboard")

    request.session["cart"] = {str(event_id): 1}
    request.session.modified = True

    return redirect("checkout")


# ==================================================
# CART PAGE
# ==================================================

@login_required
def cart_view(request):
    cart = request.session.get("cart", {})

    if not cart:
        messages.info(request, "Your cart is empty.")
        return redirect("user_dashboard")

    event_id, qty = next(iter(cart.items()))
    event = get_object_or_404(Event, id=event_id)

    total_amount = event.price * qty

    return render(request, "user/cart.html", {
        "event": event,
        "qty": qty,
        "total_amount": total_amount
    })


@login_required
def cart_inc(request, event_id):
    cart = get_cart(request)
    event = get_object_or_404(Event, id=event_id)

    if str(event_id) in cart:
        if cart[str(event_id)] < event.available_coupons:
            cart[str(event_id)] += 1
            save_cart(request, cart)
        else:
            messages.error(request, "Maximum tickets reached.")

    return redirect("cart")


@login_required
def cart_dec(request, event_id):
    cart = get_cart(request)

    if str(event_id) in cart:
        cart[str(event_id)] -= 1

        if cart[str(event_id)] <= 0:
            cart.pop(str(event_id))

        save_cart(request, cart)

    return redirect("cart")


@login_required
def cart_remove(request, event_id):
    request.session.pop("cart", None)
    request.session.modified = True
    return redirect("user_dashboard")


# ==================================================
# CHECKOUT
# ==================================================

@login_required
def checkout(request):
    cart = request.session.get("cart")

    if not cart:
        messages.info(request, "Your cart is empty.")
        return redirect("user_dashboard")

    event_id, qty = next(iter(cart.items()))
    event = get_object_or_404(Event, id=event_id)

    #  Final safety checks
    if event.event_ticket_last_purchase_date < now().date():
        messages.error(request, "Ticket sales have expired.")
        request.session.pop("cart", None)
        return redirect("user_dashboard")

    if qty > event.available_coupons:
        messages.error(request, "Not enough tickets available.")
        return redirect("cart")

    total_amount = event.price * qty

    request.session["checkout_data"] = {
        "event_id": event.id,
        "qty": qty,
        "total": float(total_amount)
    }
    request.session.modified = True

    return render(request, "user/checkout.html", {
        "event": event,
        "qty": qty,
        "total_amount": total_amount,
        "show_hero": False
    })


# ==================================================
# MY ORDERS
# ==================================================

@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user,
        order_status="PAID"
    ).select_related("event")

    return render(request, "user/my_orders.html", {
        "orders": orders
    })
