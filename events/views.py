from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from django.db.models import F
from django.contrib import messages
from django.contrib.auth import get_user_model

from .models import Event
from orders.models import Order
from tickets.models import Ticket

User = get_user_model()


# ==================================================
# USER DASHBOARD
# ==================================================

def user_dashboard(request):
    selected_status = request.GET.get("status", "active")
    selected_category = request.GET.get("category", "all")

    events = Event.objects.all()

    if selected_status == "active":
        events = events.filter(
            event_ticket_last_purchase_date__gte=now().date()
        )
    elif selected_status == "expired":
        events = events.filter(
            event_ticket_last_purchase_date__lt=now().date()
        )

    if selected_category != "all":
        events = events.filter(category=selected_category)

    categories = Event.objects.values_list(
        "category", flat=True
    ).distinct()

    return render(request, "user/user-dashboard.html", {
        "events": events,
        "categories": categories,
        "selected_status": selected_status,
        "selected_category": selected_category,
        "show_hero": True,
        "today": date.today()
    })


# ==================================================
# ADMIN DASHBOARD (ONLY OWN EVENTS + ORDERS)
# ==================================================

@login_required
def admin_dashboard(request):
    if request.user.type != "ADMIN":
        return HttpResponseForbidden("Access denied")

    admin_events = Event.objects.filter(created_by=request.user)

    admin_orders = Order.objects.filter(
        event__in=admin_events
    ).select_related("user", "event")

    context = {
        "total_events": admin_events.count(),
        "total_orders": admin_orders.count(),
        "total_tickets": Ticket.objects.filter(
            order__in=admin_orders
        ).count(),
        "total_users": admin_orders.values("user").distinct().count(),

        "recent_orders": admin_orders.order_by("-id")[:5],
    }

    return render(request, "admin/admin-dashboard.html", context)


# ==================================================
# ADMIN – EVENTS LIST
# ==================================================

@login_required
def admin_events(request):
    if request.user.type != "ADMIN":
        return HttpResponseForbidden("Access denied")

    events = Event.objects.filter(
        created_by=request.user
    ).annotate(
        tickets_sold=F("total_coupons") - F("available_coupons")
    )

    return render(request, "admin/admin-events.html", {
        "events": events
    })


# ==================================================
# ADMIN – ADD EVENT
# ==================================================

@login_required
def add_event(request):
    if request.user.type != "ADMIN":
        return HttpResponseForbidden("Access denied")

    if request.method == "POST":
        last_purchase_date = request.POST.get(
            "event_ticket_last_purchase_date"
        )

        if last_purchase_date < str(now().date()):
            messages.error(
                request,
                "Ticket last purchase date cannot be in the past."
            )
            return redirect("add_event")

        Event.objects.create(
            title=request.POST.get("title"),
            category=request.POST.get("category"),
            event_date=request.POST.get("event_date"),
            event_ticket_last_purchase_date=last_purchase_date,
            price=request.POST.get("price"),
            total_coupons=request.POST.get("total_coupons"),
            available_coupons=request.POST.get("total_coupons"),
            event_image=request.FILES.get("event_image"),
            created_by=request.user
        )

        messages.success(request, "Event added successfully.")
        return redirect("admin_events")

    return render(request, "admin/add-event.html", {
        "is_edit": False,
        "today": now().date()
    })


# ==================================================
# ADMIN – EDIT EVENT
# ==================================================

@login_required
def edit_event(request, event_id):
    if request.user.type != "ADMIN":
        return HttpResponseForbidden("Access denied")

    event = get_object_or_404(
        Event,
        id=event_id,
        created_by=request.user
    )

    if request.method == "POST":
        last_purchase_date = request.POST.get(
            "event_ticket_last_purchase_date"
        )

        if last_purchase_date < str(now().date()):
            messages.error(
                request,
                "Ticket last purchase date cannot be in the past."
            )
            return redirect("edit_event", event_id=event.id)

        event.title = request.POST.get("title")
        event.category = request.POST.get("category")
        event.event_date = request.POST.get("event_date")
        event.event_ticket_last_purchase_date = last_purchase_date
        event.price = request.POST.get("price")
        event.total_coupons = int(request.POST.get("total_coupons"))

        if event.available_coupons > event.total_coupons:
            event.available_coupons = event.total_coupons

        if request.FILES.get("event_image"):
            event.event_image = request.FILES.get("event_image")

        event.save()
        messages.success(request, "Event updated successfully.")
        return redirect("admin_events")

    return render(request, "admin/add-event.html", {
        "event": event,
        "is_edit": True,
        "today": now().date()
    })


# ==================================================
# ADMIN – DELETE EVENT
# ==================================================

@login_required
def delete_event(request, event_id):
    if request.user.type != "ADMIN":
        return HttpResponseForbidden("Access denied")

    event = get_object_or_404(
        Event,
        id=event_id,
        created_by=request.user
    )

    event.delete()
    messages.success(request, "Event deleted successfully.")
    return redirect("admin_events")
