import django_filters

from .models import Product, AttributeValue, Category, ProductType, Brand


def brands(request):
    if request is None:
        return Brand.objects.none()
    return Brand.objects.all()


def types(request):
    if request is None:
        return ProductType.objects.none()
    return ProductType.objects.all()


class ProductFilter(django_filters.FilterSet):
  sale_price = django_filters.RangeFilter()
  # product_type = django_filters.ModelChoiceFilter(queryset=types)
  # brand = django_filters.ModelChoiceFilter(choices=brands)
  # attribute_values = django_filters.filters.ModelMultipleChoiceFilter(
  #       field_name='value',
  #       to_field_name='attribute',
  #       queryset=AttributeValue.objects.all(),
  #   )
  
  class Meta:
    model = Product 
    # fields = {
    #   "name": ["icontains"], 
    #   "category__name": ["icontains"], 
    #   # "sale_price": ["lt", "gt"],
    #   "attribute_values__value": ["exact"]
    # }
    
    fields = {
      "name": ["icontains"], 
      "category": ["exact"], 
      # "sale_price": ["lt", "gt"],
      "attribute_values": ["exact"],
      "brand": ["exact"],
      "product_type": ["exact"],
    }