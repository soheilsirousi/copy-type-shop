import uuid
from django.db import models
from django.conf import settings
from order.models import Order


class Payment(models.Model):
    NOT_PAID = 0
    PAID = 1

    choices = (
        (NOT_PAID, 'Not Paid'),
        (PAID, 'Paid'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.IntegerField(default=0)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.PositiveSmallIntegerField(choices=choices, default=NOT_PAID)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)