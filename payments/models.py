from django.db import models
from orders.models import Order

class Payment(models.Model):

    STATUS_CHOICES = [
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('PENDING', 'Pending'),
    ]

    payment_gateway = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=50)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return self.transaction_id
