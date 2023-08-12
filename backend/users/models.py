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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username

    def get_shopping_list(self):
        shopping_list = []
        for name, unit, total in self.shopping_cart.values_list(
                "recipe__ingredients__ingredient__name",
                "recipe__ingredients__ingredient__measurement_unit"
                ).annotate(total_amount=models.Sum(
                "recipe__ingredients__amount")):
            shopping_list.append(f'{name}: {total} {unit}')
        return '\n'.join(shopping_list)

    def follow(self, author):
        if not self.is_following(author):
            Follower.objects.create(user=self, author=author)

    def unfollow(self, author):
        if self.is_following(author):
            Follower.objects.filter(user=self, author=author).delete()

    def is_following(self, author):
        return Follower.objects.filter(user=self, author=author).exists()


class Follower(models.Model):
    user = models.ForeignKey(User, related_name='follower',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='following',
                               on_delete=models.CASCADE)

    class Meta:
        constraints = (models.UniqueConstraint(fields=('user', 'author'),
                                               name='unique_user_author'),)
