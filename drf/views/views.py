import json
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from store.models import Product, Category
from store.serializers import ProductSerializer, CategorySerializer


@api_view(["GET", "POST"])
def product_alt_view(request, slug=None, *args, **kwargs):
  method = request.method
  if method == "GET":
    if slug is not None:
      # Detail View 
      instance = get_object_or_404(Product, slug=slug)
      data = ProductSerializer(instance).data 
      return Response(data)
      
    queryset = Product.objects.all()
    data = ProductSerializer(queryset, many=True).data 
    return Response(data)
  elif method == "POST":
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      data = serializer.data
      return Response(data)


@api_view(["GET"])
def product_detail(request, *args, **kwargs):
  slug = kwargs["slug"]
  instance = Product.objects.get(slug=slug)
  data = ProductSerializer(instance).data
  return Response(data)


@api_view(["GET"])
def categories(request, *args, **kwargs):
  instance = Category.objects.all()
  
  data = {}
  if instance:
    for cat in instance:
      data[str(cat.id)] = CategorySerializer(cat).data
  return Response(data)


@api_view(["GET"])
def category_detail(request, *args, **kwargs):
  slug = kwargs["slug"]
  instance = Category.objects.get(slug=slug)
  data = CategorySerializer(instance).data
  return Response(data)


@api_view(["POST"])
def category_create(request, *args, **kwargs):
  data = request.data 
  serializer = CategorySerializer(data=request.data)
  if serializer.is_valid(raise_exception=True):
    data = serializer.data
    return Response(data)
  



