from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views import generic
from django.contrib import messages

from .models import Cart, CartItem, CartItemAttribute
from .forms import ShippingForm

from store.models import Product, AttributeValue
from account.forms import UserAddressForm
from order.models import Order, OrderItem

from decimal import Decimal


# Create your views here.
@login_required
@require_POST
def cart_add(request):
  attribute_values = []
  for key in request.POST.keys():
    if key.startswith("attr_"):
      attribute_values.append(request.POST.get(key))
  quantity = request.POST.get("quantity")
  prod_id = request.POST.get("product")
  
  try:
    item = CartItem.objects.get(cart=request.user.cart, product_id=prod_id)
    if item:
      item.quantity += int(quantity)
      item.save()
  except:
    item = CartItem.objects.create(
      cart=request.user.cart, 
      product_id=prod_id, quantity=quantity)
  attributes = AttributeValue.objects.filter(attribute_values__product__pk=prod_id, value__in=attribute_values)
  
  for attr in attributes:
    CartItemAttribute.objects.get_or_create(item=item, attribute_value=attr)
  messages.success(request, "Added to cart successfully")
  return render(request, "partials/header.html", {"cart": request.user.cart})


class CartListView(generic.TemplateView):
  template_name = "cart/shoping-cart.html"
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["addr_form"] = ShippingForm()
    context["new_addr"] = UserAddressForm()
    return context 
  
  def post(self, request, *args, **kwargs):
    print(request.POST.dict)
    # try:
    #   for key, value in request.POST.items():
    #     try:
    #       item = get_object_or_404(CartItem, id=int(key))
    #       item.quantity = int(value)
    #       item.save()
    #     except:
    #       pass 
    #     else:
    #       messages.success(request, "Cart updated successful")
  # except:
    if request.POST.get("address"):
      addr_id = request.POST.get("address")
    else:
      form = UserAddressForm(request.POST)
      if form.is_valid():
        addr = form.save(commit=False)
        addr.customer=request.user 
        addr.save()
      addr_id = addr.pk
    if addr_id:
      amount = Decimal(request.user.cart.subtotal())
      order = Order.objects.create(user=request.user, amount=amount, address_id=addr_id)
      
      items = CartItem.objects.filter(cart=request.user.cart)
      for item in items:
        OrderItem.objects.create(
          order=order, product=item.product,
          price=item.price, 
          quantity=item.quantity)
      messages.success(request, "Order successful")
    return redirect(request.META["HTTP_REFERER"])