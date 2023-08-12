from django.core.exceptions import ValidationError
import re


def validate_tag_slug(value):
    pattern = r'^[-a-zA-Z0-9_]+$'
    if not re.match(pattern, value):
        raise ValidationError('Некорректный HEX код.',
                              params={'value': value})


def validate_recipe_cooking_time(value):
    if value < 1:
        raise ValidationError('Время не может быть меньше одной минуты.',
                              params={'value': value})


def validate_ingredientInRecipe_amount(value):
    if value <= 0:
        raise ValidationError('Неверное количество ингредиентов.',
                              params={'value': value})
