from django.urls import path
from .views import add_event, admin_events

urlpatterns = [
    path('dashboard/events/', admin_events, name='admin_events'),
    path('dashboard/events/add/', add_event, name='add_event'),
]
