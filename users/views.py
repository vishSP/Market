from rest_framework.generics import UpdateAPIView, CreateAPIView

from users.models import User
from users.serializers import UserSerializer


class ProfileUpdateView(UpdateAPIView):
    model = User
    serializer_class = UserSerializer

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateAPIView):
    model = User
    serializer_class = UserSerializer
