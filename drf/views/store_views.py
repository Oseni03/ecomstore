from django.utils.text import slugify

from rest_framework import generics, mixins
from rest_framework import permissions
from rest_framework import authentication 

from store.models import Product, Category
from store.serializers import ProductSerializer, CategorySerializer
from store.permissions import IsStaffEditorPermission

from drf.authentication import TokenAuthentication


class ProductListCreateAPIView(generics.ListCreateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer 
  authentication_classes = [
    authentication.SessionAuthentication,
    TokenAuthentication,
  ]
  permission_classes = [IsStaffEditorPermission]

 
class ProductDetailAPIView(generics.RetrieveAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer 
  lookup_field = "slug"

 
class ProductUpdateAPIView(generics.UpdateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer 
  lookup_field = "slug"

 
class ProductDeleteAPIView(generics.DestroyAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer 
  lookup_field = "slug"
  permission_class = []
  
  def perform_destroy(self, instance):
    # Instance 
    super().perform_destroy(instance)


class CategoryListCreateAPIView(generics.ListCreateAPIView):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer 
  
  def perform_create(self, serializer):
    # serializer.save(parent=parent)
    name = serializer.validated_data.get("name")
    slug = serializer.validated_data.get("slug")
    if slug is None:
      slug = slugify(name)
    serializer.save(slug=slug)

 
class CategoryDetailAPIView(generics.RetrieveAPIView):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer 
  lookup_field = "slug"

 
class CategoryUpdateAPIView(generics.UpdateAPIView):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer 
  lookup_field = "slug"
  
  def perform_update(self, serializer):
    # Instance 
    super().perform_update(serializer)

  
class CategoryDeleteAPIView(generics.DestroyAPIView):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer 
  lookup_field = "slug"
  
  def perform_destroy(self, instance):
    # Instance 
    super().perform_destroy(instance)


# All CRUD functionality
class ProductMixinView(
  mixins.DestroyModelMixin,
  mixins.CreateModelMixin,
  mixins.ListModelMixin, 
  mixins.RetrieveModelMixin,
  generics.GenericAPIView
  ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 
    lookup_field = "slug"
    
    def get(self, request, *args, **kwargs):
      slug = kwargs.get("slug")
      if slug is not None:
        return self.retrieve(request, *args, **kwargs)
      return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
      return self.create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
      return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
      return self.destroy(request, *args, **kwargs)