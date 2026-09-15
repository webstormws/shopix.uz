from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.ImageField(source="product.image", read_only=True)
    price = serializers.DecimalField(source="product.price", max_digits=12, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_name", "product_image", "price", "quantity", "subtotal"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items", "total"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "price", "quantity", "subtotal"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    market_name = serializers.CharField(source="market.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "user", "market", "market_name", "status", "status_display",
            "payment_method", "is_paid", "address", "location_lat", "location_lng",
            "total", "items", "created_at", "updated_at",
        ]
        read_only_fields = ["user", "total", "is_paid"]


class CheckoutSerializer(serializers.Serializer):
    """Buyurtma rasmiylashtirish (checkout) uchun kiruvchi ma'lumot."""
    address = serializers.CharField(max_length=255)
    location_lat = serializers.FloatField(required=False, allow_null=True)
    location_lng = serializers.FloatField(required=False, allow_null=True)
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES, default="card")
    card_id = serializers.IntegerField(required=False, allow_null=True)  # SavedCard id — karta orqali to'lov
