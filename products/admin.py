from django.contrib import admin
from .models import Product, Category, Brand, ProductImage, ProductVariant

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "brand",
        "price",
        "is_active",
    ]

    search_fields = [
        "name",
    ]

    list_filter = [
        "brand",
        "category",
        "is_active"

    ]

    prepopulated_fields = {
        "slug":("name", )
    }
