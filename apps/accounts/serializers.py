from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import SavedCard

User = get_user_model()


class SavedCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedCard
        fields = ["id", "card_holder", "card_number_masked", "expiry", "is_default", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    """Profilni ko'rsatish / tahrirlash uchun (rasm, manzil, lokatsiya kiritilgan)."""
    cards = SavedCardSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "first_name", "last_name", "email", "phone",
            "avatar", "address", "location_lat", "location_lng",
            "is_seller", "date_joined", "cards",
        ]
        read_only_fields = ["id", "date_joined"]


class RegisterSerializer(serializers.ModelSerializer):
    """Ro'yxatdan o'tish (register)."""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Parollar mos emas"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Standart JWT login serializer, lekin javobga foydalanuvchi ma'lumotini ham qo'shamiz —
    shunda React tomonda alohida so'rov yubormasdan foydalanuvchini olamiz.
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data
