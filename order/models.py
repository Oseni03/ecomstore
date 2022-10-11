from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from account.models import Address
from store.models import Product
from coupon.models import Coupon

import secrets

# Create your models here.
class Order(models.Model):
  # each individual status 
  SUBMITTED = 1 
  PROCESSED = 2 
  SHIPPED = 3 
  CANCELLED = 4 
  # set of possible order statuses 
  ORDER_STATUSES = (
    (SUBMITTED,'Submitted'), 
    (PROCESSED,'Processed'),
    (SHIPPED,'Shipped'), 
    (CANCELLED,'Cancelled'),)
  
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "orders")
  address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  amount = models.DecimalField(max_digits=6, decimal_places=2)
  ref_code = models.CharField(max_length=200)
  status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
  coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
  discount = models.IntegerField(default=0, 
    validators=[MinValueValidator(0), 
    MaxValueValidator(100)])
  
  class Meta:
    ordering = ("-created_at",)
  
  def __str__(self):
    return str(self.id)
  
  def save(self, *args, **kwargs) -> None:
    while not self.ref_code:
      ref = secrets.token_urlsafe(50)
      obj = Order.objects.filter(ref_code=ref)
      if not obj:
        self.ref_code = ref 
    super().save(*args, **kwargs)
  

class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
  price = models.DecimalField(max_digits=6, decimal_places=2)
  quantity = models.PositiveIntegerField(default=1)
  
  def __str__(self):
    return str(self.id)