from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsReviewOwner
from .models import Product, Category, Brand, ProductVariant, ProductImage, Review
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, ProductVariantSerializer, ProductImageSerializer, ReviewSerializer

class AdminOrReadOnlyViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action in ["list", "retrieve",]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


class BrandViewSet(AdminOrReadOnlyViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "slug"

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


class CategoryViewSet(AdminOrReadOnlyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"

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


class ProductViewSet(AdminOrReadOnlyViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"

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
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return super().get_queryset()

        return super().get_queryset().filter(is_active=True)


class ProductImageViewSet(AdminOrReadOnlyViewSet):
    queryset = ProductImage.objects.all()
    serializer = ProductImageSerializer

    filterset_fields = [
        DjangoFilterBackend,
        SearchFilter
    ]

    search_fields = [
        "product",
        "is_primary"
    ]


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

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]

    filterset_fields = [
        "product",
    ]

    ordering_fields = [
        "created_at",
        "rating",
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ["list", "retrieve",]:
            permission_classes = [AllowAny]
        elif self.action in ["create"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated,
                                  IsReviewOwner,]

        return [permission() for permission in permission_classes]
