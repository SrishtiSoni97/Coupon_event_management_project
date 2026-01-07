from django.db import models
from orders.models import Order
from accounts.models import Users

class Ticket(models.Model):

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('REDEEMED', 'Redeemed'),
    ]

    ticket_code = models.CharField(
        max_length=50,
        unique=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    is_used = models.BooleanField(default=False)

    redeemed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='tickets'
    )

    redeemed_by = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='redeemed_tickets'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tickets'

    def __str__(self):
        return self.ticket_code
