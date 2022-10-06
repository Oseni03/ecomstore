from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Review(models.Model):
  product = models.ForeignKey(settings.REVIEW_PRODUCT_MODEL, on_delete=models.CASCADE, related_name = "reviews")
  name = models.CharField(max_length=150, verbose_name=_("User name"))
  email = models.EmailField(verbose_name=_("User email"), max_length=150)
  content = models.TextField(verbose_name=_("Content"))
  rating = models.PositiveSmallIntegerField(default=1, verbose_name=_("Rating"))
  created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("date product image created"), help_text=_("format: y-m-d H:M:S"))
  is_active = models.BooleanField(default=True)
  
  class Meta:
    verbose_name_plural = _('Reviews')
    ordering = ('-created_at',)
  
  def __str__(self):
    return f"{self.name} - {self.rating}"
  
  def range(self):
    return range(self.rating)