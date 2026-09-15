from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import SavedCard
from .serializers import (
    RegisterSerializer, UserSerializer, MyTokenObtainPairSerializer, SavedCardSerializer,
)

User = get_user_model()


class UserListView(generics.ListAPIView):
    """GET /api/accounts/users/  — faqat admin/admin uchun foydalanuvchilar ro'yxati."""
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("-date_joined")


class RegisterView(generics.CreateAPIView):
    """POST /api/accounts/register/  — yangi foydalanuvchi ro'yxatdan o'tadi."""
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    """POST /api/accounts/login/  — login qilib access/refresh token va user ma'lumotini qaytaradi."""
    serializer_class = MyTokenObtainPairSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/accounts/profile/ — profil ma'lumotlari, lokatsiya, avatar shu yerdan yangilanadi."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class SavedCardListCreateView(generics.ListCreateAPIView):
    """Foydalanuvchining to'lov kartalari — Karta ID bilan to'lash uchun."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SavedCardSerializer

    def get_queryset(self):
        return SavedCard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavedCardDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SavedCardSerializer

    def get_queryset(self):
        return SavedCard.objects.filter(user=self.request.user)
