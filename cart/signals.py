from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import Customer

from .models import Cart

@receiver(post_save, sender=Customer)
def cart_creator(sender, instance, created, **kwargs):
  if created:
    Cart.objects.create(user=instance)