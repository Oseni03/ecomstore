from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import CustomAccountManager

from .models import Cart

@receiver(post_save, sender=CustomAccountManager)
def cart_creator(sender, instance, created, **kwargs):
  if created:
    Cart.objects.create(user=instance)