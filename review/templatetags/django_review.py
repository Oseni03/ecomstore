from django import template

from review.forms import ReviewForm
from review.models import Review

register = template.Library()

@register.inclusion_tag('review/product_reviews.html')
def reviews(product):
  return {
    "reviews": Review.objects.filter(product=product, is_active=True),
    "form": ReviewForm(),
    "product": product,
  }

