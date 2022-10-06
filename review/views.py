from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings

from .forms import ReviewForm
from .models import Review

# Create your views here.
@require_POST
def review_submit(request):
  pk = request.POST.get("product_id")
  form = ReviewForm(request.POST)
  if form.is_valid():
    review = form.save(commit=False)
    review.product_id = pk
    review.save()
  context = {
    "reviews": Review.objects.filter(product_id=pk, is_active=True),
    "form": ReviewForm(),
    "product": review.product
  }
  return render(request, "review/product_reviews.html", context)
  
# redirect(request.POST.get('path'))