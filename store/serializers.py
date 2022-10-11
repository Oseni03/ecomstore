from .models import Product, Category

from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
  category = serializers.SerializerMethodField(read_only=True)
  
  class Meta:
    model = Product 
    fields = ["sku", "name", "slug", "description", "store_price", "sale_price", "discount_price", "weight", "in_stock", "category"]
  
  def get_category(self, obj):
    # if not hasattr(obj, "sku"):
    #   return None 
    if not isinstance(obj, Product):
      return None 
    return str(obj.category.first().name)


class CategorySerializer(serializers.ModelSerializer):
  parent = serializers.SerializerMethodField(read_only=True)
  
  class Meta:
    model = Category 
    fields = ["name", "slug", "parent", "is_active"]
  
  def get_parent(self, obj):
    if not isinstance(obj, Category):
      return None
    try:
      return str(obj.parent.name)
    except:
      return None