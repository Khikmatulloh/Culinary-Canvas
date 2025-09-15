import uuid
import logging
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import User
from .serializers import RegisterSerializer, UserSerializer
from .tasks import send_confirmation_email

logger = logging.getLogger(__name__)
User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    """
    POST /api/users/register/  -> create user (inactive until email confirmed)
    """
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Userni yaratamiz
        user = serializer.save(is_active=False)

        # Token yaratish va Redis'ga saqlash
        token = str(uuid.uuid4())
        cache.set(token, user.id, timeout=3600)  # 1 soat amal qiladi

        # Celery orqali email yuborish
        send_confirmation_email.delay(user.email, token)

        logger.info("New user registered (inactive): %s", user.email)

        return Response(
            {"message": "User registered. Please check your email to confirm."},
            status=status.HTTP_201_CREATED
        )


class ConfirmEmailView(APIView):
    """
    GET /api/users/confirm/<token>/ -> confirm user email
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, token):
        user_id = cache.get(token)
        if not user_id:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        user.is_active = True
        user.save()
        cache.delete(token)

        logger.info("User confirmed email: %s", user.email)

        return Response(
            {"message": "Email confirmed successfully. You can now login."},
            status=status.HTTP_200_OK
        )


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    GET/PUT /api/users/me/ -> get or update current user's profile
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
