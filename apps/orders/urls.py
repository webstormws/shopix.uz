from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CartView, CartAddItemView, CartUpdateItemView, CheckoutView,
    OrderViewSet, OrderStatusUpdateView,
)

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/", CartAddItemView.as_view(), name="cart-add"),
    path("cart/items/<int:pk>/", CartUpdateItemView.as_view(), name="cart-item"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("orders/<int:pk>/status/", OrderStatusUpdateView.as_view(), name="order-status"),
] + router.urls
