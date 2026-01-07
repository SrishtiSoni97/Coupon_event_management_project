from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 🔐 hashes password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('type', 'ADMIN')

        return self.create_user(email, password, **extra_fields)


class Users(AbstractUser):

    USER_TYPE_CHOICE = [
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    ]

    username = None  
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)

    type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICE,
        default='USER'
    )
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    EMAIL_FIELD = 'email'

    objects = CustomUserManager()  

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email
