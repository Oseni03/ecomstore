from .models import Cart

def cart(request):
  try:
    cart = Cart.objects.prefetch_related(
      "items__product__media", 
      "items__attributes__attribute_value").filter(user=request.user).get()
  except:
    cart = None
  return {
    "cart": cart,
  }