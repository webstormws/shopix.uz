from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SavedCard


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Admin panelda qo'shimcha maydonlarni ko'rsatish
    list_display = ("username", "email", "phone", "is_seller", "is_staff", "created_at")
    fieldsets = UserAdmin.fieldsets + (
        ("Qo'shimcha ma'lumot", {"fields": ("phone", "avatar", "address", "location_lat", "location_lng", "is_seller")}),
    )


@admin.register(SavedCard)
class SavedCardAdmin(admin.ModelAdmin):
    list_display = ("user", "card_holder", "card_number_masked", "is_default")
