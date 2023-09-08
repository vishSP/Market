import re

from django.core.exceptions import ValidationError


class PhoneValidator:
    phone_regex = r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$'
    massage = "Телефон должен быть в формате: +7(***)***-**-**"

    def __call__(self, value):
        if not re.match(self.phone_regex, value):
            raise ValidationError(massage=self.massage)


class PasswordValidator:
    def call(self, value):
        if len(value) < 8:
            raise ValidationError('Пароль должен быть не менее 8 символов.')
        if not re.search(r'[A-Z]', value):
            raise ValidationError('Пароль должен содержать хотя бы один символ верхнего регистра.')
        if not re.search(r'[a-zA-Z]', value):
            raise ValidationError('Пароль должен содержать только символы латиницы.')
        if not re.search(r'[$%&!:.]', value):
            raise ValidationError('Пароль должен содержать хотя бы один спец символ из $%&!:.')
