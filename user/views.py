from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.db import transaction
from datetime import datetime, timezone
from rest_framework_simplejwt.exceptions import TokenError

from shared.utils.ip_addr import get_client_ip
from .serializers import UserSerializer, LoginSerializer, LoginRefreshSerializer
from .models import UserSession
from shared.utils.response import success_response, error_response


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            ip_addr = get_client_ip(request)
            ua = request.user_agent

            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            email = serializer.validated_data.get("email", "")
            password = serializer.validated_data.get("password", "")

            user = authenticate(request=request, email=email, password=password)
            if not user:
                return error_response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    message="Invalid email or password",
                )

            if not user.is_active:
                return error_response(
                    status=status.HTTP_403_FORBIDDEN,
                    message="Account is disabled",
                )

            if not user.email_verified:
                return error_response(
                    status=status.HTTP_403_FORBIDDEN,
                    message="Your email needs to be verified!",
                )

            with transaction.atomic():
                refresh = RefreshToken.for_user(user)
                refresh_jti = refresh["jti"]
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)

                UserSession.objects.create(
                    user=user,
                    ip_address=ip_addr,
                    jti=refresh_jti,
                    expires_at=datetime.fromtimestamp(refresh["exp"], tz=timezone.utc),
                    is_active=True,
                    user_agent=request.headers.get("User-Agent", ""),
                    device_type=(
                        ua.device.family if ua.device.family != "Other" else "Desktop"
                    ),
                    browser=str(ua.browser.family),
                    os=str(ua.os.family),
                )
                update_last_login(None, user)

            serializer = UserSerializer(user)

            return success_response(
                status=status.HTTP_200_OK,
                message="User logged in",
                data={
                    "user": serializer.data,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
            )

        except Exception as e:
            return error_response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal Server error",
                errors=[str(e)],
            )


class LoginRefreshAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LoginRefreshSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            refresh = RefreshToken(serializer.validated_data.get("refresh_token"))
            jti = refresh["jti"]
            user_session = UserSession.objects.select_related("user").get(
                jti=jti, is_active=True
            )

            if not user_session.user.is_active:
                return error_response(
                    status=status.HTTP_403_FORBIDDEN,
                    message="User is disabled, please contact support!",
                )
            if not user_session.user.email_verified:
                return error_response(
                    status=status.HTTP_403_FORBIDDEN,
                    message="Email not verified for this user",
                )

            access_token = str(refresh.access_token)

            return success_response(
                status=status.HTTP_200_OK,
                message="Token generated",
                data={"access_token": access_token, "refresh_token": str(refresh)},
            )

        except UserSession.DoesNotExist:
            return error_response(
                status=status.HTTP_404_NOT_FOUND,
                message="user session not found! Login again.",
            )
        except TokenError:
            return error_response(
                status=status.HTTP_401_UNAUTHORIZED,
                message="Invalid or expired refresh token",
            )
        except Exception as e:
            return error_response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal Server error",
                errors=[str(e)],
            )
