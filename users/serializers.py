from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from .validators import PasswordValidator, PhoneValidator


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Настроена проверка номера телефона.
    Телефонный номер должен быть в формате: +7(9**)***-**-**
    """
    password2 = serializers.CharField()

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if not password == password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            patronymic=validated_data["patronymic"],
            phone=validated_data["phone"], )

        user.set_password(validated_data["password"])
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


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
