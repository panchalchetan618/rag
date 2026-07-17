from rest_framework import serializers

from shared.serializers import BaseModelSerializer
from .models import User, UserSession


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    password = serializers.CharField(
        required=True,
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )

    def validate_email(self, value):
        return value.strip().lower()


class LoginRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "public_id",
            "last_login",
            "first_name",
            "last_name",
            "email",
            "email_verified",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "public_id": {"read_only": True},
        }


class UserSessionSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = UserSession
