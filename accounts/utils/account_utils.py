from django.contrib.auth import authenticate
from accounts.models import Users

def validate_required_fields(data: dict) -> bool:
   
    return all(value for value in data.values())

def is_email_exists(email):
    
    return Users.objects.filter(email=email).exists()

def create_user(first_name, last_name, email, mobile, password, user_type):
    user = Users.objects.create_user(
        email=email,
        password=password,
        mobile=mobile
    )
    user.first_name = first_name
    user.last_name = last_name
    user.type = user_type  # USER or ADMIN
    user.save()
    return user




def authenticate_user(request, email, password):
    return authenticate(request, username=email, password=password)


def is_admin(user):
   
    return user.type == 'ADMIN'
