from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Tag, Ingredient, Recipe, IngredientInRecipe, FavoriteRecipe
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
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'tags', 'author', 'ingredients', 'image', 'is_favorited', 'is_in_shopping_cart']

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        if not user.is_authenticated:
            return False
        return FavoriteRecipe.objects.filter(user=user, recipe=obj).exists()


    def get_is_in_shopping_cart(self, obj):
        return False

class FavoriteRecipeSerializer(ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')
        validators = [UniqueTogetherValidator(queryset=FavoriteRecipe.objects.all(),
                      fields=('user', 'recipe'), message='рецепт уже есть в избранном')
        ]