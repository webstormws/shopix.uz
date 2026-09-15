from django.contrib import admin
from .models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("path", "ip_address", "user", "created_at")
    list_filter = ("path",)