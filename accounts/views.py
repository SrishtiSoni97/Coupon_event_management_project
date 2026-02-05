from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from accounts.utils.account_utils import (
    validate_required_fields,
    is_email_exists,
    create_user,
    authenticate_user,
    is_admin
)

def register_view(request):
    if request.method == 'POST':
        data = {
            "first_name": request.POST.get('first_name'),
            "last_name": request.POST.get('last_name'),
            "email": request.POST.get('email'),
            "mobile": request.POST.get('mobile'),
            "password": request.POST.get('password'),
            "type": request.POST.get('type'),
        }

        if not validate_required_fields(data):
            messages.error(request, "All fields are required")
            return render(request, "auth/register.html")

        if is_email_exists(data["email"]):
            messages.error(request, "Email already exists")
            return render(request, "auth/register.html")

        create_user(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            mobile=data["mobile"],
            password=data["password"],
            user_type=data["type"],
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "auth/register.html")





def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate_user(request, email, password)

        if user:
            login(request, user)

            if is_admin(user):
                return redirect('admin_dashboard')

            return redirect('user_dashboard')

        
        messages.error(
            request,
            "Invalid email or password. Please try again."
        )
        return redirect("login")

    return render(request, 'auth/login.html')


        

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        return HttpResponseForbidden("Access denied")

    return render(request, 'admin/admin-dashboard.html')


# @login_required
# def user_dashboard(request):
#     return render(request, 'user/user-dashboard.html')
