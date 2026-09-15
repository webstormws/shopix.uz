from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "total", "created_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("created_at",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "subtotal")
    search_fields = ("cart__user__username", "product__name")
    list_filter = ("cart",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product_name", "price", "quantity", "subtotal")
    readonly_fields = ("subtotal",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "market", "status", "payment_method", "is_paid", "total", "created_at")
    list_filter = ("status", "payment_method", "is_paid", "market")
    search_fields = ("user__username", "user__email", "market__name", "address")
    list_editable = ("status", "is_paid")
    inlines = [OrderItemInline]
    ordering = ("-created_at",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_name", "price", "quantity", "subtotal")
    search_fields = ("product_name", "order__user__username")
    list_filter = ("order__status",)
