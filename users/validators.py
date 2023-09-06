import re

from django.core.exceptions import ValidationError


class PhoneValidator:
    phone_regex = r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$'
    massage = "Телефон должен быть в формате: +7(***)***-**-**"

    def __call__(self, value):
        if not re.match(self.phone_regex, value):
            raise ValidationError(massage=self.massage)

class PasswordValidator:
    def __call__(self, value):
        """
        Проверяет, содержит ли пароль и буквы, и цифры.
        """
        if not any(char.isdigit() for char in value):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру.")
        if not any(char.isalpha() for char in value):
            raise ValidationError("Пароль должен содержать хотя бы одну букву.")