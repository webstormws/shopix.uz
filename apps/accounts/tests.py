from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.catalog.models import Category, Market, Product
from apps.orders.models import Cart, CartItem
from .serializers import RegisterSerializer


class AuthAndCartFlowTests(TestCase):
    def test_register_serializer_creates_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "phone": "998901234567",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
        }

        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()

        self.assertEqual(user.username, "newuser")
        self.assertTrue(user.check_password("StrongPass123!"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_cart_total_uses_item_prices_and_quantity(self):
        category = Category.objects.create(name="Test Category", slug="test-category")
        market = Market.objects.create(name="Test Market", address="Tashkent")
        product = Product.objects.create(
            market=market,
            category=category,
            name="Test Product",
            price=25000,
            unit="kg",
        )
        user = User.objects.create_user(username="buyer", password="StrongPass123!")
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=3)

        self.assertEqual(cart.total, 75000)


User = get_user_model()
