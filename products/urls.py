from rest_framework.routers import DefaultRouter
from .views import BrandViewSet,  CategoryViewSet, ProductViewSet, ProductImageViewSet, ProductVariantViewSet, ReviewViewSet


router = DefaultRouter()
router.register("brand", BrandViewSet)
router.register("category", CategoryViewSet)
router.register("products", ProductViewSet)
router.register("images", ProductImageViewSet)
router.register("variant", ProductVariantViewSet)
router.register("review", ReviewViewSet)
urlpatterns = router.urls
