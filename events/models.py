from django.db import models
from accounts.models import Users

class Event(models.Model):

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
    ]

    title = models.CharField(max_length=100)
    category = models.CharField(max_length=150)
    event_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    event_image = models.ImageField(
        upload_to='events/',
        null=True,
        blank=True
    )

    total_coupons = models.PositiveIntegerField()
    available_coupons = models.PositiveIntegerField()

    event_ticket_last_purchase_date=models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    created_by = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='events'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'events'

    def __str__(self):
        return self.title
