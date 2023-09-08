from typing import Any, Dict

from rest_framework import serializers

from .models import User
from .validators import PasswordValidator, PhoneValidator


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя.

    Настроена проверка номера телефона.
    Телефонный номер должен быть в формате: +7(9**)***-**-**
    """

    password = serializers.CharField(
        write_only=True, required=True, validators=[PasswordValidator()]
    )
    phone = serializers.CharField(validators=[PhoneValidator()])

    class Meta:
        model = User
        fields = ["id", "email", "password", "first_name", "last_name", "phone", "patronymic"]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "patronymic": {"required": True},
            "phone": {"required": True},
        }

    def create(self, validated_data: Dict[str, Any]) -> User:
        user = User.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            patronymic=validated_data["patronymic"],
            phone=validated_data["phone"],

        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CustomUser, представляющей пользователей.
    """

    phone = serializers.CharField(validators=[PhoneValidator()])

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "patronymic", "id", "email"]
        read_only_fields = ["id", "email"]
