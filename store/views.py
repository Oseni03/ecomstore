from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator
from django.urls import reverse

from .models import Product, ProductAttributeValues
from .filters import ProductFilter

# Create your views here.
class HomeView(generic.ListView):
  template_name = "store/home.html"
  queryset = Product.objects.prefetch_related(
    "category", "product_type", 
    "attribute_values", "media").filter(is_active=True)
  context_object_name = "products"
  paginate_by = 9
  
  def get_templates(self):
    if self.request.htmx:
      return "store/partials/product_list.html"
    else:
      return super().get_templates()
  
  def get_queryset(self, **kwargs):
    queryset = super().get_queryset()
    self.filterset = ProductFilter(self.request.GET, queryset=queryset)
    return self.filterset.qs 
  
  def get_context_data(self):
    context = super().get_context_data()
    context["form"] = self.filterset.form
    context["url"] = reverse("store:home")
    return context


class ProductDetailView(generic.DetailView):
  template_name = 'store/product-detail.html'
  queryset = Product.objects.prefetch_related(
    "category", "product_type__attributes", 
    "attribute_values", "media").filter(is_active=True)
  context_object_name = "product"
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data()
    context["attributes"] = self.get_object().product_type.attributes.all()
    return context
  
  def get_templates(self):
    if self.request.htmx:
      return "store/partials/modal1.html"
    else:
      return super().get_templates()


class ShopView(generic.ListView):
  template_name = "store/product.html"
  queryset = Product.objects.prefetch_related(
    "category", "product_type", 
    "attribute_values", "media").filter(is_active=True)
  context_object_name = "products"
  paginate_by = 12
  
  def get_queryset(self, **kwargs):
    queryset = super().get_queryset()
    self.filterset = ProductFilter(self.request.GET, queryset=queryset)
    return self.filterset.qs 
  
  def get_context_data(self):
    context = super().get_context_data()
    context["form"] = self.filterset.form
    context["url"] = reverse("store:shop")
    return context
