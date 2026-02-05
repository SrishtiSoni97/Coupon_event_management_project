from django.urls import path
from . import views

urlpatterns = [
    # User payment flow
    path("", views.payment_page, name="payment"),
    path("stripe-session/", views.create_stripe_session, name="stripe_session"),
    path("success/", views.payment_success, name="payment_success"),
    path("fail/", views.payment_fail, name="payment_fail"),

    # 🔥 Stripe webhook (VERY IMPORTANT)
    path("stripe-webhook/", views.stripe_webhook, name="stripe_webhook"),
]
