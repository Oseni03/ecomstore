from django.shortcuts import render
from django.views import generic

from order.models import Order

# Create your views here.
class OrderListView(generic.ListView):
  template_name = "order/orders.html" 
  context_object_name = "orders"
  
  def get_queryset(self):
    return Order.objects.filter(user=self.request.user)