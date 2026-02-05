from django.urls import path
from .views import (
    user_dashboard,
    admin_dashboard,
    admin_events,
    add_event,
    edit_event,
    delete_event,
)

urlpatterns = [
    # USER
    path("user-dashboard/", user_dashboard, name="user_dashboard"),

    # ADMIN
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("dashboard/events/", admin_events, name="admin_events"),
    path("dashboard/events/add/", add_event, name="add_event"),
    path("dashboard/events/edit/<int:event_id>/", edit_event, name="edit_event"),
    path("dashboard/events/delete/<int:event_id>/", delete_event, name="delete_event"),
]
