from rest_framework.serializers import ModelSerializer, SerializerMethodField

from recipes.models import Tag, Ingredient, Recipe, IngredientInRecipe
from users.models import User
class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']

class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']

class IngredientInRecipeSerializer(ModelSerializer):
    measurement_unit = SerializerMethodField()
    name = SerializerMethodField()
    id = SerializerMethodField()
    class Meta:
        model = IngredientInRecipe
        fields = ['id', 'amount', 'measurement_unit', 'name']

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit
    def get_name(self, obj):
        return obj.ingredient.name

    def get_id(self, obj):
        return obj.ingredient.id

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'last_name', 'first_name']

class RecipeSerializer(ModelSerializer):

    tags = TagSerializer(many=True)
    ingredients = IngredientInRecipeSerializer(many=True)
    author = UserSerializer(read_only=True)
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'tags', 'author', 'ingredients', 'image', ]

