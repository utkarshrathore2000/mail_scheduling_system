from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "user_type",
        )
        extra_kwargs = {
            "username": {"required": True, "allow_blank": False},
            "email": {"required": True, "allow_blank": False},
            "password": {"required": True, "allow_blank": False},
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "user_type": {"required": True, "allow_blank": False},
        }

    def create(self, validated_data):
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        user_type = validated_data.get("user_type")
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
        )
        return user