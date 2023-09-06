from django.views.generic import UpdateView, CreateView

from users.forms import UserForm, UserRegisterForm
from users.models import User
from users.serializers import UserSerializer


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm
    serializer_class = UserSerializer

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        return response
