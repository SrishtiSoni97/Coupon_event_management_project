from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:event_id>/", views.add_to_cart, name="add_to_cart"),

    # ✅ ADD THIS
    path("buy-now/<int:event_id>/", views.buy_now, name="buy_now"),

    path("cart/inc/<int:event_id>/", views.cart_inc, name="cart_inc"),
    path("cart/dec/<int:event_id>/", views.cart_dec, name="cart_dec"),
    path("cart/remove/<int:event_id>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("my-orders/", views.my_orders, name="my_orders"),
]
