from django.db import models

from users.models import User
from recipes.validators import validate_recipe_cooking_time, validate_tag_slug, validate_ingredient_counter
class Tag(models.Model):

    name = models.CharField(max_length=200, unique=True, db_index=True)
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(unique=True, validators=[validate_tag_slug])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Recipe(models.Model):
    author = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='recipes/', null=True)
    text = models.TextField()
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

class CountIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='ingredient_counter', on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[validate_ingredient_counter])

    class Meta:
        constraints = (models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_recipe_ingredient'),)


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, related_name='favorite', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='in_favorites', on_delete=models.CASCADE)

    class Meta:
        constraints = (models.UniqueConstraint(fields=('user', 'recipe'), name='unique_user_recipe'),)