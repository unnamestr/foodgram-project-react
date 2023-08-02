from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, filters
from django.shortcuts import get_object_or_404

from recipes.models import Tag, Ingredient, Recipe, FavoriteRecipe
from api.serializers import TagSerializer, IngredientSerializer, RecipeSerializer, FavoriteRecipeSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class FavoriteRecipeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, recipe_id):
        serializer = FavoriteRecipeSerializer(data={'user': request.user.id, 'recipe': recipe_id})
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
        pass

    def delete(self, request, recipe_id):
        pass

@api_view(['GET',])
def download_shopping_cart(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."},
                        status=status.HTTP_401_UNAUTHORIZED)
    user = request.user
    return Response(status=status.HTTP_200_OK)