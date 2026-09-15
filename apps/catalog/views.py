from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Market, Product, Review
from .serializers import (
    CategorySerializer, MarketSerializer, ProductListSerializer,
    ProductDetailSerializer, ReviewSerializer,
)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Hamma o'qiy oladi (GET), lekin faqat admin/sotuvchi o'zgartira oladi."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_seller)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class MarketViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "address"]


class ProductViewSet(viewsets.ModelViewSet):
    """
    Mahsulotlar bo'yicha to'liq CRUD.
    Filtrlash: ?category=1&market=2&search=pomidor&ordering=price
    Bular Uzum Market kabi qidiruv/filter funksiyasi uchun kerak.
    """
    queryset = Product.objects.filter(is_active=True).select_related("market", "category")
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "market"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Mahsulotga izoh/komment qoldirish (faqat login qilganlar)."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
