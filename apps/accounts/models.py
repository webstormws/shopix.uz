"""
Foydalanuvchi (User) modeli.
Django'ning standart User modelini kengaytiramiz: telefon, rasm, manzil, lokatsiya.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Uzum Market kabi: telefon raqami asosiy identifikator sifatida ham ishlatiladi
    phone = models.CharField(max_length=20, blank=True, unique=False, verbose_name="Telefon")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Profil rasmi")
    address = models.CharField(max_length=255, blank=True, verbose_name="Manzil")

    # Profildagi lokatsiya (xarita uchun) — rasm(dagi) profil bo'limidagi kabi
    location_lat = models.FloatField(blank=True, null=True, verbose_name="Kenglik (lat)")
    location_lng = models.FloatField(blank=True, null=True, verbose_name="Uzunlik (lng)")

    is_seller = models.BooleanField(default=False, verbose_name="Sotuvchi/Do'kon egasi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class SavedCard(models.Model):
    """
    Foydalanuvchi to'lov kartalari (Karta ID bilan ishlash uchun).
    Xavfsizlik: haqiqiy loyihada karta raqami hech qachon to'liq saqlanmaydi,
    faqat tokenlashtirilgan (masked) shakli saqlanadi.
    """
    user = models.ForeignKey(User, related_name="cards", on_delete=models.CASCADE)
    card_holder = models.CharField(max_length=120, verbose_name="Karta egasi")
    card_number_masked = models.CharField(max_length=25, verbose_name="Karta raqami (masked) 8600 **** **** 1234")
    expiry = models.CharField(max_length=5, verbose_name="Amal qilish muddati MM/YY")
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_holder} - {self.card_number_masked}"
