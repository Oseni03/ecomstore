from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.sessions.backends.db import SessionStore

from store.models import Product, AttributeValue
from account.models import Customer
from coupon.models import Coupon

from decimal import Decimal

exposed_request = None


# Create your models here.
class Cart(models.Model):
  user = models.OneToOneField(Customer, related_name="cart", on_delete=models.CASCADE)
  total = models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("date cart created"), help_text=_("format: y-m-d H:M:S"))
  updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("date cart updated"), help_text=_("format: y-m-d H:M:S"))
  
  class Meta:
    verbose_name = _("cart")
    verbose_name_plural = _("carts")
  
  def __str__(self):
    return self.user.name
  
  def subtotal(self):
    return Decimal(sum(item.price for item in self.items.all()))
    
  @property
  def coupon(self):
    coupon_id = exposed_request.session.get("coupon_id")
    if coupon_id:
      return Coupon.objects.get(id=coupon_id)
    return None 
  
  def get_discount(self):
    if self.coupon:
      return (self.coupon.discount / Decimal("100")) * self.subtotal()
    return Decimal("0")
  
  def get_final_price(self):
    return self.subtotal() - self.get_discount()
  
  def update_total(self):
    self.total = sum(item.quantity for item in self.items.all())
    self.save()


class CartItem(models.Model):
  cart = models.ForeignKey(
    Cart, related_name="items", 
    on_delete=models.SET_NULL, null=True)
  quantity = models.IntegerField(default=1)
  product = models.ForeignKey(Product, 
    related_name="cart_items", 
    on_delete=models.CASCADE)
  added_at = models.DateTimeField(
    auto_now_add=True, editable=False, 
    verbose_name=_("date cart-item added"), 
    help_text=_("format: y-m-d H:M:S"))
  updated_at = models.DateTimeField(
    auto_now=True, editable=False, 
    verbose_name=_("date cart-item updated"), 
    help_text=_("format: y-m-d H:M:S"))
  price = models.DecimalField(
        max_digits=7, decimal_places=2, 
        default = 0.00,
        verbose_name=_("total price"), 
        help_text=_("format: maximum price 999.99"), 
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 9999.99."),
            },
        },)
  
  class Meta:
    verbose_name = _("cart item")
    verbose_name_plural = _("cart items")
    unique_together = (("cart", "product"))
  
  def __str__(self):
    return str(self.product.name)
  
  def save(self, *args, **kwargs):
    ans = int(self.quantity) * self.product.sale_price
    self.price = Decimal(ans)
    self.cart.update_total()
    
    if self.quantity == 0:
      self.delete()
    super().save(*args, **kwargs)


class CartItemAttribute(models.Model):
  item = models.ForeignKey(
    CartItem, related_name="attributes", 
    on_delete=models.CASCADE)
  attribute_value = models.ForeignKey(
    AttributeValue, related_name="items", 
    on_delete=models.SET_NULL, null=True)
  
  class Meta:
    unique_together = (("item", "attribute_value"))