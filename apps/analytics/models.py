"""
Saytga necha kishi kirgani va foydalanganini kuzatish uchun (admin dashboard grafigi uchun).
"""
from django.conf import settings
from django.db import models


class Visit(models.Model):
    path = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.path} - {self.created_at}"

