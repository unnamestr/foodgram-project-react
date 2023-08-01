from rest_framework.serializers import ModelSerializer

from recipes.models import Tag, Ingredient, Recipe, CountIngredient

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']

class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']

class CountIngredientSerializer(ModelSerializer):
    class Meta:
        model = CountIngredient
        fields = '__all__'

class RecipeSerializer(ModelSerializer):

    tags = TagSerializer(many=True)
    ingredients = CountIngredientSerializer(many=True)
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'tags', 'author', 'ingredients', 'image', ]