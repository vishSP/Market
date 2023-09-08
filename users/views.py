from django.views.generic import UpdateView, CreateView

from users.models import User
from users.serializers import UserSerializer


class ProfileUpdateView(UpdateView):
    model = User
    serializer_class = UserSerializer

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    model = User
    serializer_class = UserSerializer
