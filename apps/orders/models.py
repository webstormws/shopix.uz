"""
Savatcha (Cart), Buyurtma (Order) va To'lov (Payment).
Rasmdagi "Buyurtma #4587" kuzatuv (tracking) bo'limiga mos status maydonlari bor.
"""
from django.conf import settings
from django.db import models
from apps.catalog.models import Product, Market


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"{self.user} savatchasi"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"


class Order(models.Model):
    """Buyurtma — checkout tugagach shu yerga yoziladi va status bosqichma-bosqich o'zgaradi."""

    STATUS_CHOICES = [
        ("new", "Qabul qilindi"),
        ("preparing", "Tayyorlanmoqda"),
        ("on_the_way", "Yo'lda"),
        ("delivered", "Yetkazib berildi"),
        ("cancelled", "Bekor qilindi"),
    ]
    PAYMENT_CHOICES = [
        ("card", "Karta orqali"),
        ("cash", "Naqd pul"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    market = models.ForeignKey(Market, on_delete=models.SET_NULL, null=True, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="card")
    is_paid = models.BooleanField(default=False)

    address = models.CharField(max_length=255, verbose_name="Yetkazib berish manzili")
    location_lat = models.FloatField(blank=True, null=True)
    location_lng = models.FloatField(blank=True, null=True)

    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)  # buyurtma vaqtidagi nomi (saqlanadi)
    price = models.DecimalField(max_digits=12, decimal_places=2)  # buyurtma vaqtidagi narxi
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
