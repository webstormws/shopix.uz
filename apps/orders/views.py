from django.db import transaction
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.response import Response

from apps.catalog.models import Product
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, OrderSerializer, CheckoutSerializer


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartView(views.APIView):
    """GET /api/orders/cart/ — joriy foydalanuvchi savatchasini olish."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        return Response(CartSerializer(cart).data)


class CartAddItemView(views.APIView):
    """POST /api/orders/cart/add/  body: {product: id, quantity: 1} — savatga mahsulot qo'shish."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_or_create_cart(request.user)
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))
        product = Product.objects.filter(id=product_id, is_active=True).first()
        if not product:
            return Response({"detail": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity})
        if not created:
            item.quantity += quantity
            item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class CartUpdateItemView(views.APIView):
    """PATCH /api/orders/cart/items/<id>/  body: {quantity: n} — miqdorni o'zgartirish."""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        item = CartItem.objects.filter(id=pk, cart__user=request.user).first()
        if not item:
            return Response({"detail": "Topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        quantity = int(request.data.get("quantity", item.quantity))
        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()
        return Response(CartSerializer(item.cart if quantity > 0 else get_or_create_cart(request.user)).data)

    def delete(self, request, pk):
        item = CartItem.objects.filter(id=pk, cart__user=request.user).first()
        if item:
            cart = item.cart
            item.delete()
            return Response(CartSerializer(cart).data)
        return Response({"detail": "Topilmadi"}, status=status.HTTP_404_NOT_FOUND)


class CheckoutView(views.APIView):
    """
    POST /api/orders/checkout/
    Savatchadagi mahsulotlardan buyurtma (Order) yaratadi — "Buyurtma rasmiylashtirish" tugmasi shu yerga ulanadi.
    """
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        cart = get_or_create_cart(request.user)
        cart_items = cart.items.select_related("product", "product__market").all()
        if not cart_items:
            return Response({"detail": "Savatcha bo'sh"}, status=status.HTTP_400_BAD_REQUEST)

        # Hozircha bitta buyurtma bitta do'kondan deb hisoblaymiz (birinchi mahsulot do'koni)
        market = cart_items[0].product.market

        order = Order.objects.create(
            user=request.user,
            market=market,
            address=data["address"],
            location_lat=data.get("location_lat"),
            location_lng=data.get("location_lng"),
            payment_method=data["payment_method"],
            is_paid=(data["payment_method"] == "card"),  # karta bilan darhol to'langan deb simulyatsiya qilamiz
            total=cart.total,
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order, product=item.product, product_name=item.product.name,
                price=item.product.price, quantity=item.quantity,
            )
        cart_items.delete()  # savatchani bo'shatish

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/orders/orders/         -> foydalanuvchining o'z buyurtmalari
    GET /api/orders/orders/<id>/    -> buyurtma tafsiloti (kuzatuv/tracking uchun)
    Admin/sotuvchi bo'lsa hammasini ko'radi.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_seller:
            return Order.objects.all()
        return Order.objects.filter(user=user)


class OrderStatusUpdateView(views.APIView):
    """PATCH /api/orders/orders/<id>/status/ body:{status: 'on_the_way'} — faqat admin/sotuvchi status yangilaydi."""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        if not (request.user.is_staff or request.user.is_seller):
            return Response({"detail": "Ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)
        order = Order.objects.filter(id=pk).first()
        if not order:
            return Response({"detail": "Topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        new_status = request.data.get("status")
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({"detail": "Noto'g'ri status"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)