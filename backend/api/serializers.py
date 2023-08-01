from rest_framework.serializers import ModelSerializer

from recipes.models import Tag, Ingredient, Recipe

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']

class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']

class RecipeSerializer(ModelSerializer):

    tags = TagSerializer(many=True)
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'tags', 'author', 'ingredients', 'image', ]