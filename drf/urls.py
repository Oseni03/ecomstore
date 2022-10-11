from django.urls import path, include

from .views import store_views
from .views import views

app_name = "drf"

urlpatterns = [
  # path("product/", store_views.ProductListCreateAPIView.as_view(), name="products"),
  # path("product/<slug:slug>/", store_views.ProductDetailAPIView.as_view(), name="product-detail"),
  # path("product/<slug:slug>/update/", store_views.ProductUpdateAPIView.as_view(), name="product-update"),
  # path("product/<slug:slug>/delete/", store_views.ProductDeleteAPIView.as_view(), name="product-delete"),
  path("product/", store_views.ProductMixinView.as_view(), name="products"),
  path("product/<slug:slug>/", store_views.ProductMixinView.as_view(), name="product-detail"),
  path("product/<slug:slug>/update/", store_views.ProductMixinView.as_view(), name="product-update"),
  path("product/<slug:slug>/delete/", store_views.ProductMixinView.as_view(), name="product-delete"),
  
  path("category/", store_views.CategoryListCreateAPIView.as_view(), 
    name="categories"),
  path("category/<slug:slug>/", 
    store_views.CategoryDetailAPIView.as_view(), name="category-detail"),
  path("category/<slug:slug>/update/", 
    store_views.CategoryUpdateAPIView.as_view(), name="category-update"),
  path("category/<slug:slug>/delete/", 
    store_views.CategoryDeleteAPIView.as_view(), name="category-delete"),
  
  
  # path("product/", views.product_alt_view, name="products"),
  # path("product/<slug:slug>/", views.product_alt_view, name="detail"),
  # path("category/create/", store_views.CategoryCreateAPIView.as_view(), 
  #   name="category-create"),
]