from django.contrib import admin

from .models import Cart, CartItem, CartItemAttribute

# Register your models here.
admin.site.register(CartItemAttribute)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
  list_display = ["__str__", "quantity"]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
  list_display = ["__str__", "total"]