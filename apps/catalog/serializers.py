from rest_framework import serializers
from .models import Category, Market, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "icon"]


class MarketSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source="products.count", read_only=True)

    class Meta:
        model = Market
        fields = [
            "id", "name", "logo", "address", "rating", "reviews_count",
            "open_time", "close_time", "location_lat", "location_lng",
            "is_open", "products_count",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    avatar = serializers.ImageField(source="user.avatar", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "product", "user", "username", "avatar", "rating", "comment", "created_at"]
        read_only_fields = ["user"]


class ProductListSerializer(serializers.ModelSerializer):
    """Ro'yxat (list) uchun yengil serializer."""
    market_name = serializers.CharField(source="market.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "image", "price", "old_price", "unit", "stock",
            "market", "market_name", "category", "category_name", "is_active",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Bitta mahsulot uchun to'liq ma'lumot + izohlar (comments)."""
    market = MarketSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "image", "price", "old_price", "unit", "stock",
            "description", "market", "category", "reviews", "average_rating",
            "is_active", "created_at",
        ]

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        return round(sum(r.rating for r in reviews) / len(reviews), 1)
