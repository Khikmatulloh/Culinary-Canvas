from django.urls import path
from .views import RegisterAPIView, ProfileAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "users"

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("me/", ProfileAPIView.as_view(), name="me"),
    # JWT endpoints (you can also expose these at project-level urls)
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]