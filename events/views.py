from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Event


from django.db.models import F

@login_required
def add_event(request):
    if request.user.type != 'ADMIN':
        return HttpResponseForbidden("Access denied")

    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        event_date = request.POST.get('event_date')
        price = request.POST.get('price')
        total_coupons = request.POST.get('total_coupons')
        image = request.FILES.get('event_image')

        event = Event.objects.create(
            title=title,
            category=category,
            event_date=event_date,
            price=price,
            total_coupons=total_coupons,
            available_coupons=total_coupons,
            created_by=request.user,
            event_image=image
        )

        return redirect('admin_events')

    return render(request, 'admin/add-event.html')





@login_required
def admin_events(request):
    if request.user.type != 'ADMIN':
        return HttpResponseForbidden("Access denied")

    events = Event.objects.annotate(
        tickets_sold=F('total_coupons') - F('available_coupons')
    )

    return render(request, 'admin/admin-events.html', {
        'events': events
    })