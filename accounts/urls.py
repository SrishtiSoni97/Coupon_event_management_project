from django.urls import path 

from .views import login_view, register_view, logout_view, admin_dashboard

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/',register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
#     path('user-dashboard/', user_dashboard, name='user_dashboard'),
 ]