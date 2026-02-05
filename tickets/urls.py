from django.urls import path
from . import views

app_name = "tickets"

urlpatterns = [
    path("my-tickets/", views.my_ticket_events, name="my_ticket_events"),
    path("my-tickets/<int:event_id>/", views.my_tickets_by_event, name="my_tickets_by_event"),
]
