import re

from django.core.exceptions import ValidationError


class PhoneValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, field):
        message = "Телефон должен быть в формате: +7(***)***-**-**"
        phone_regex = r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$'
        if not re.match(phone_regex, str(field)):
            raise ValidationError(message=message)


class PasswordValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, field):
        if len(field) < 8:
            raise ValidationError('Пароль должен быть не менее 8 символов.')
        if not re.search(r'[A-Z]', str(field)):
            raise ValidationError('Пароль должен содержать хотя бы один символ верхнего регистра.')
        if not re.search(r'[a-zA-Z]', str(field)):
            raise ValidationError('Пароль должен содержать только символы латиницы.')
        if not re.search(r'[$%&!:.]', str(field)):
            raise ValidationError('Пароль должен содержать хотя бы один спец символ из $%&!:.')
