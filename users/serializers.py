from rest_framework import serializers

from .models import User
from .validators import PasswordValidator, PhoneValidator


class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if not password == password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def save(self, **kwargs):
        user = User.objects.create(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            patronymic=self.validated_data["patronymic"],
            phone=self.validated_data["phone"], )

        user.set_password(self.validated_data["password"])
        user.save()

        return user

    class Meta:
        model = User
        fields = ["id", "email", "password", "password2", "first_name", "last_name", "phone", "patronymic"]
        ref_name = 'UserModel'
        validators = [PasswordValidator(field='password'), PhoneValidator(field='phone')]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "patronymic": {"required": True},
            "phone": {"required": True},
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CustomUser, представляющей пользователей.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "patronymic", "id", "email"]
        read_only_fields = ["id", "email"]
        validators = [PhoneValidator(field='phone')]
