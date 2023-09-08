import os

from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from djoser.conf import settings
from users.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class UserCreationTestCase(APITestCase): # pragma: no cover
    """Регистрация пользователя"""

    def setUp(self):
        self.register_url = "register/"
        self.valid_user_data = {
            "email": "ivan@mail.com",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "patronymic":"Ivanovich",
            "password": "Qwerty12345!",
            "phone": "+7(912)345-67-89",
        }
        self.invalid_phone_user_data = self.valid_user_data.copy()
        self.invalid_phone_user_data["phone"] = "892134567891"

        self.invalid_password_user_data = self.valid_user_data.copy()
        self.invalid_password_user_data["password"] = "Qazwsxedcrfv"


    def test_invalid_phone_number(self):
        """Некорректный номер телефона"""
        response = self.client.post(
            self.register_url, self.invalid_phone_user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("phone", response.data)

        self.assertEqual(User.objects.count(), 0)

    def test_invalid_password(self):
        """Некорректный пароль"""
        response = self.client.post(
            self.register_url, self.invalid_password_user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("password", response.data)

        self.assertEqual(User.objects.count(), 0)


