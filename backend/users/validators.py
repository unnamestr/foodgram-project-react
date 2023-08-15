import re

from django.core.exceptions import ValidationError


def validate_username(value):
    pattern = r'^[\w.@+-]+\Z'
    if value.lower() == 'me' or not re.match(pattern, value):
        raise ValidationError('Некорректный username',
                              params={'value': value})
