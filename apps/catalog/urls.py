from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, MarketViewSet, ProductViewSet, ReviewViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("markets", MarketViewSet, basename="market")
router.register("products", ProductViewSet, basename="product")
router.register("reviews", ReviewViewSet, basename="review")

urlpatterns = router.urls
