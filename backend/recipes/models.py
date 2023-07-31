from django.db import models

from users.models import User
from recipes.validators import validate_recipe_cooking_time, validate_tag_color
class Tag(models.Model):

    name = models.CharField(max_length=200, unique=True, db_index=True)
    color = models.CharField(max_length=7, unique=True, validators=[validate_tag_color])
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Recipes(models.Model):
    author = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='recipes/', null=True)
    text = models.TextField()
    #ingredients
    tags = models.ManyToManyField(Tag)
    cooking_time = models.IntegerField(validators=[validate_recipe_cooking_time])
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Ingredient(models.Model):

    name = models.CharField(max_length=200, unique=True)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']