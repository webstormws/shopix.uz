from django.contrib import admin
from .models import Category, Market, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "rating", "is_open", "owner")
    list_filter = ("is_open",)
    search_fields = ("name", "address")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "market", "category", "price", "stock", "is_active")
    list_filter = ("market", "category", "is_active")
    search_fields = ("name",)
    list_editable = ("price", "stock", "is_active")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
