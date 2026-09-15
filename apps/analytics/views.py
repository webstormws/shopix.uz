from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework import permissions, views
from rest_framework.response import Response

from apps.orders.models import Order
from apps.catalog.models import Product
from .models import Visit

User = get_user_model()


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_seller)


class DashboardStatsView(views.APIView):
    """
    GET /api/analytics/dashboard/
    Admin panel uchun asosiy statistika: rasmdagi "Admin panel" bo'limiga mos
    (buyurtmalar soni, foydalanuvchilar, kunlik statistikalar, so'nggi buyurtmalar).
    """
    permission_classes = [IsAdminOnly]

    def get(self, request):
        today = timezone.now().date()
        last_30_days = today - timedelta(days=30)

        orders_qs = Order.objects.all()

        # Kunlar bo'yicha buyurtmalar statistikasi (chart uchun)
        daily_stats = []
        for i in range(13, -1, -1):
            day = today - timedelta(days=i)
            count = orders_qs.filter(created_at__date=day).count()
            revenue = orders_qs.filter(created_at__date=day, is_paid=True).aggregate(s=Sum("total"))["s"] or 0
            daily_stats.append({"date": day.strftime("%Y-%m-%d"), "orders": count, "revenue": float(revenue)})

        data = {
            "total_users": User.objects.count(),
            "total_products": Product.objects.count(),
            "total_orders": orders_qs.count(),
            "total_revenue": float(orders_qs.filter(is_paid=True).aggregate(s=Sum("total"))["s"] or 0),
            "visits_today": Visit.objects.filter(created_at__date=today).count(),
            "visits_last_30_days": Visit.objects.filter(created_at__date__gte=last_30_days).count(),
            "unique_visitors_today": Visit.objects.filter(created_at__date=today).values("ip_address").distinct().count(),
            "orders_by_status": list(orders_qs.values("status").annotate(count=Count("id"))),
            "daily_stats": daily_stats,
            "recent_orders": list(
                orders_qs.order_by("-created_at")[:8].values(
                    "id", "user__username", "status", "total", "created_at"
                )
            ),
        }
        return Response(data)
