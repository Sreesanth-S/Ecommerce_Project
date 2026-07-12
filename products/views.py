from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product, Category, Brand, ProductVariant
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, ProductVariantSerializer

class AdminOrReadOnlyViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action in ["list", "retrieve",]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

class ProductViewSet(AdminOrReadOnlyViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "category",
        "brand",
        "is_featured",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "price",
        "created_at",
    ]

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()

        return super().get_queryset().filter(is_active=True)


class CategoryViewSet(AdminOrReadOnlyViewSet):
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    search_fields = [
        "name",
    ]

    filterset_fields = [
        "name",
    ]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BrandViewSet(AdminOrReadOnlyViewSet):
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = [
        "name",
    ]

    search_fields = [
        "name",
    ]

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductVariantViewSet(AdminOrReadOnlyViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "color",
        "size",
        "product",
        "storage",
        "is_active"
    ]

    search_fields = [
        "sku",
        "color",
        "size",
        "storage",
    ]

    ordering_fields = [
        "price",
        "stock",
    ]
