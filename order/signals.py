from django.dispatch import receiver
from django.db.models.signals import post_save

from order.models import Order


@receiver(post_save, sender=Order)
def complete_time(sender, instance, update_fields, **kwargs):
    pass