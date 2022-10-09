from .models import Cart

def cart(request):
  return {
    "cart": Cart.objects.prefetch_related(
      "items__product__media", 
      "items__attributes__attribute_value").filter(user=request.user).get(),
  }