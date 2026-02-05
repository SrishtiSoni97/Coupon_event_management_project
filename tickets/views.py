from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now

from orders.models import Order
from events.models import Event


# ======================================================
# 1️⃣ ORIGINAL VIEW (ALL TICKETS - YOUR EXISTING LOGIC)
# ======================================================
@login_required
def my_tickets(request):
    """
    Shows ALL tickets purchased by the user (across all events).
    Used as fallback / legacy view.
    """

    orders = (
        Order.objects
        .filter(user=request.user, order_status="PAID")
        .select_related("event")
        .prefetch_related("tickets")
        .order_by("-created_at")
    )

    return render(request, "user/my_tickets.html", {
        "orders": orders,
        "event": None   # Important for template reuse
    })


# ======================================================
#  EVENT-WISE LIST (CLICK EVENT → SEE TICKETS)
@login_required
def my_ticket_events(request):
    """
    Shows list of EVENTS for which the user has purchased tickets.
    Clicking an event opens event-wise tickets.
    """

    events = (
        Event.objects
        .filter(
            orders__user=request.user,
            orders__order_status="PAID"
        )
        .distinct()
        .order_by("event_date")
    )

    return render(request, "user/my_ticket_events.html", {
        "events": events
    })


# ======================================================
# 3️⃣ EVENT-SPECIFIC TICKETS
# ======================================================
@login_required



@login_required
def my_tickets_by_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    today = now().date()

    orders = (
        Order.objects
        .filter(
            user=request.user,
            event=event,
            order_status="PAID"
        )
        .prefetch_related("tickets")
    )

    active_tickets = []
    expired_tickets = []

    for order in orders:
        for ticket in order.tickets.all():
            if event.event_date >= today and not ticket.is_used:
                active_tickets.append(ticket)
            else:
                expired_tickets.append(ticket)

    return render(request, "user/my_tickets_by_event.html", {
        "event": event,
        "active_tickets": active_tickets,
        "expired_tickets": expired_tickets,
    })
