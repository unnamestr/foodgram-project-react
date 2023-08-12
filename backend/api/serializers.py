from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField,
                                        Serializer, CharField,
                                        ValidationError,
                                        PrimaryKeyRelatedField,
                                        IntegerField)
from rest_framework.validators import UniqueTogetherValidator
from drf_extra_fields.fields import Base64ImageField
from django.utils.translation import gettext_lazy as _

from recipes.models import (Tag, Ingredient, Recipe, IngredientInRecipe,
                            FavoriteRecipe, ShoppingCart)
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
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'last_name', 'first_name',
                  'is_subscribed']

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        return False if not user.is_authenticated else user.is_following(obj)


class RecipeBaseSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class RecipeSerializer(RecipeBaseSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientInRecipeSerializer(many=True)
    author = UserSerializer(read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta(RecipeBaseSerializer.Meta):
        fields = RecipeBaseSerializer.Meta.fields + ['tags', 'author',
                                                     'ingredients',
                                                     'is_favorited',
                                                     'is_in_shopping_cart']

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        if not user.is_authenticated:
            return False
        return FavoriteRecipe.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user
        if not user.is_authenticated:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class FavoriteRecipeSerializer(ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')
        validators = [UniqueTogetherValidator(
            queryset=FavoriteRecipe.objects.all(), fields=('user', 'recipe'),
            message='рецепт уже есть в избранном')]

    def to_representation(self, obj):
        recipe = obj.recipe
        request = self.context.get('request')
        image_url = request.build_absolute_uri(recipe.image.url)
        return {'id': recipe.id, 'name': recipe.name, 'image': image_url,
                'cooking_time': recipe.cooking_time}


class ShoppingCartSerializer(ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        validators = [UniqueTogetherValidator(
                      queryset=ShoppingCart.objects.all(),
                      fields=('user', 'recipe'),
                      message='рецепт уже есть в списке покупок')]

    def to_representation(self, obj):
        recipe = obj.recipe
        request = self.context.get('request')
        image_url = request.build_absolute_uri(recipe.image.url)
        return {'id': recipe.id, 'name': recipe.name, 'image': image_url,
                'cooking_time': recipe.cooking_time}


class PasswordSerializer(Serializer):
    new_password = CharField(required=True)
    current_password = CharField(required=True)

    def validate_current_password(self, current_password):
        user = self.context['request'].user
        if user.check_password(current_password):
            return current_password
        raise ValidationError('The data provided is incorrect')

    def validate_new_password(self, new_password):
        validate_password(new_password)
        return new_password


class UserWithRecipeSerializer(UserSerializer):
    recipes_count = SerializerMethodField(read_only=True)
    recipes = SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ["recipes", "recipes_count"]

    def get_recipes(self, obj):
        query = obj.recipes.all()
        if self.context.get("recipes_limit"):
            query = query[:int(self.context.get("recipes_limit"))]
        serializer = RecipeBaseSerializer(query, many=True,
                                          context={"request":
                                                   self.context.get("request")
                                                   })
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class CreateIngredientInRecipeSerializer(Serializer):
    id = IntegerField()
    amount = IntegerField()


class CreateRecipeSerializer(ModelSerializer):
    ingredients = CreateIngredientInRecipeSerializer(many=True)
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(),
                                  error_messages={
                                      'does_not_exist': _('invalid tag id')})
    image = Base64ImageField(use_url=True, max_length=None)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'image', 'ingredients', 'name',
                  'text', 'cooking_time']

    def validate_ingredients(self, data):
        if len(data) == 0:
            raise ValidationError('Need ingredients')
        uniq_ingredient = set()
        for item in data:
            if item['id'] not in uniq_ingredient:
                if not Ingredient.objects.filter(id=item['id']).exists():
                    raise ValidationError('ingredient not found.')
                uniq_ingredient.add(item['id'])
            else:
                raise ValidationError('Use uniq ingredients')
        return data

    def validate_cooking_time(self, value):
        if value < 1:
            raise ValidationError('time cannot be less than 1')
        return value

    def create(self, data):
        ingredients = data.pop('ingredients')
        tags = data.pop('tags')
        recipe = Recipe.objects.create(author=self.context.get('request').user,
                                       **data)
        recipe.tags.set(tags)
        [IngredientInRecipe.objects.create(ingredient_id=i['id'],
                                           amount=i['amount'],
                                           recipe=recipe) for i in ingredients]
        return recipe

    def update(self, obj, data):
        IngredientInRecipe.objects.filter(recipe=obj).delete()
        obj.tags.clear()
        obj.tags.set(data.pop('tags'))
        ingredients = data.pop('ingredients')
        [IngredientInRecipe.objects.create(ingredient_id=i['id'],
                                           amount=i['amount'],
                                           recipe=obj) for i in ingredients]
        return super().update(obj, data)

    def to_representation(self, instance):
        r = self.context.get('request')
        return RecipeSerializer(instance, context={'request': r}).data
