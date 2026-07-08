from django.contrib import admin
from .models import Product, Category, Brand, ProductImage, ProductVariant

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)
