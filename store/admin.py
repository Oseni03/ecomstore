from django.contrib import admin
from .models import Stock, Media, AttributeValue, Brand, Attribute, Product, Category, ProductAttributeValues, ProductType, ProductTypeAttribute


admin.site.register(ProductAttributeValues)
admin.site.register(Brand)


class TypeAttributeInline(admin.TabularInline):
    model = ProductTypeAttribute 


class StockInline(admin.TabularInline):
    model = Stock 


class MediaInline(admin.TabularInline):
    model = Media 


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue 


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [
        AttributeValueInline
    ]


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        TypeAttributeInline
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("name",),
    }
    list_per_page = 50


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [StockInline, MediaInline]
    prepopulated_fields = {
        "slug": ("name",),
    }
    list_filter = (
      ('category', admin.RelatedOnlyFieldListFilter),
      ("is_active", admin.BooleanFieldListFilter), 
      ("is_featured", admin.BooleanFieldListFilter), 
      ("is_bestseller", admin.BooleanFieldListFilter), 
      ('brand', admin.RelatedOnlyFieldListFilter),
      ('product_type', admin.RelatedOnlyFieldListFilter),
    )
    list_per_page = 50
    
    search_fields = ['category']
    list_display = ('__str__', 'product_type', "brand", "sale_price")
    list_select_related = ('product_type', "brand", 'stock')
