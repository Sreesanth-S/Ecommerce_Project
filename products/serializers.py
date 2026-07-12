from rest_framework import serializers
from django.db.models import Avg
from .models import Product, Category, Brand, ProductVariant, Review, ProductImage

class ProductSerializer(serializers.ModelSerializer):
    class BrandSerializer(serializers.ModelSerializer):
        class Meta:
            model = Brand
            fields = ["id", "name", "slug", "logo"]

    class CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ["id", "name", "slug"]

    class ProductImageSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductImage
            fields = ["id", "image", "is_primary"]

    class ProductVariantSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductVariant
            fields = [
                "id",
                "sku",
                "color",
                "size",
                "storage",
                "price",
                "stock"
            ]

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "category",
            "category_id",
            "brand",
            "brand_id",
            "price",
            "sale_price",
            "discount_percentage",
            "images",
            "variants",
            "average_rating",
            "review_count",
            "is_featured",
        ]

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        source="category",
        write_only=True
    )
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset = Brand.objects.all(),
        source = "brand",
        write_only = True
    )
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    discount_percentage = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    def get_discount_percentage(self, obj):
        if not obj.sale_price:
            return 0

        return round(((obj.price - obj.sale_price)/obj.price) * 100, 2)

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(
            Avg("rating")
        )["rating__avg"]
        return round(avg, 1) if avg else 0

    def get_review_count(self, obj):
        return obj.reviews.count()

    def validate(self, attrs):
        price  = attrs.get("price")
        sale = attrs.get("sale_price")

        if sale and sale > price:
            raise serializers.ValidationError("Sale price cannot exceed price")

        return attrs

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = "__all__"

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "product",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = ["user"]

    def validate(self, attrs):
        user = self.context["request"].user
        product = attrs.get("product")

        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("You have already reviewed this product")

        return attrs
