from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, filters
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin

from recipes.models import Tag, Ingredient, Recipe, FavoriteRecipe, ShoppingCart
from users.models import User
from api.serializers import TagSerializer, IngredientSerializer, RecipeSerializer, FavoriteRecipeSerializer, \
    ShoppingCartSerializer, UserSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class FavoriteRecipeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, recipe_id):
        serializer = FavoriteRecipeSerializer(data={'user': request.user.id, 'recipe': recipe_id},
                                              context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        user_id = request.user.id
        if not FavoriteRecipe.objects.filter(user=user_id, recipe=recipe_id).exists():
            return Response({"errors": "рецепта нет в избранном"}, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        FavoriteRecipe.objects.filter(user=user_id, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, recipe_id):
        serializer = ShoppingCartSerializer(data={'user': request.user.id, 'recipe': recipe_id},
                                            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        user_id = request.user.id
        if not ShoppingCart.objects.filter(user=user_id, recipe=recipe_id).exists():
            return Response({"errors": "рецепта нет в списке покупок"}, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShoppingCart.objects.filter(user=user_id, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', ])
def download_shopping_cart(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."},
                        status=status.HTTP_401_UNAUTHORIZED)
    user = request.user
    filename = 'shopping_list.txt'
    response = HttpResponse(user.get_shopping_list(), content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


class UserViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
