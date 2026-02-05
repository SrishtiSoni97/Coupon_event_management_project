from django.db import models
from accounts.models import Users
from events.models import Event

class Order(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ]

    order_code = models.CharField(
        max_length=50,
        unique=True
    )

    quantity = models.PositiveIntegerField()

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    order_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return self.order_code
