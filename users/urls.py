from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users.apps import UsersConfig
from users.views import ProfileUpdateView, RegisterAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
