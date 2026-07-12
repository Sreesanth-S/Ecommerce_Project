from django.db import models
from accounts.models import Users
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to="brand_logos/",
                             blank=True,
                             null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10,
                                         decimal_places=2,
                                         blank=True,
                                         null=True)
    brand = models.ForeignKey(Brand,
                              on_delete=models.CASCADE,
                              related_name="products")
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    class Meta:
        constraints = [models.UniqueConstraint(fields=["product", "color", "size", "storage"],
                                               name="unique_product_variants")]

    product = models.ForeignKey(Product,
                               on_delete=models.CASCADE,
                               related_name="variants")
    sku = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=30, blank=True)
    size = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    storage = models.CharField(max_length=30, blank=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product} ({self.color}, {self.size}, {self.storage})"


class ProductImage(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="images")
    image = models.ImageField(upload_to="products_images/")
    is_primary = models.BooleanField(default=True)

    def __str__(self):
        return self.image.name


class Review(models.Model):
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "product"],
                                               name="unique_review")]

    user = models.ForeignKey(Users,
                             on_delete=models.CASCADE,
                             related_name="reviews")
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="reviews")
    rating = models.DecimalField(max_digits =2,
                                 decimal_places=1,
                                 validators=[MinValueValidator(1),
                                             MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - ({self.product.name})"
