"""
Katalog: Kategoriyalar, Do'konlar (marketlar) va Mahsulotlar.
Rasmdagi "Kategoriyalar" va "Do'konlar" bo'limlariga mos.
"""
from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    slug = models.SlugField(unique=True, blank=True)
    icon = models.ImageField(upload_to="categories/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Kategoriyalar"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Market(models.Model):
    """Do'kon / market — masalan Makro, Korzinka, Havas kabi."""
    name = models.CharField(max_length=150, verbose_name="Do'kon nomi")
    logo = models.ImageField(upload_to="markets/", blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    reviews_count = models.PositiveIntegerField(default=0)
    open_time = models.TimeField(default="09:00")
    close_time = models.TimeField(default="23:00")
    location_lat = models.FloatField(blank=True, null=True)
    location_lng = models.FloatField(blank=True, null=True)
    is_open = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="markets")

    class Meta:
        verbose_name_plural = "Do'konlar"

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [("kg", "kg"), ("dona", "dona"), ("litr", "litr"), ("pachka", "pachka")]

    market = models.ForeignKey(Market, related_name="products", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, verbose_name="Mahsulot nomi")
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi (so'm)")
    old_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Chegirmagacha narx")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="dona")
    stock = models.PositiveIntegerField(default=100, verbose_name="Ombordagi soni")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.price} so'm/{self.unit}"


class Review(models.Model):
    """Mahsulot yoki do'kon uchun izoh/komment va reyting."""
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(default=5)  # 1-5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} -> {self.product} ({self.rating})"
