from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_username


class User(AbstractUser):
    username = models.CharField(max_length=150, blank=False, unique=True,
                                validators=(validate_username,))
    password = models.CharField(max_length=150, blank=False)
    email = models.EmailField(max_length=254, blank=False, unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    def get_shopping_list(self):
        shopping_list = []
        for name, unit, total in self.shopping_cart.values_list(
                "recipe__ingredients__ingredient__name",
                "recipe__ingredients__ingredient__measurement_unit").annotate(
                total_amount=models.Sum("recipe__ingredients__amount")):
            shopping_list.append(f'{name}: {total} {unit}')
        return '\n'.join(shopping_list)
