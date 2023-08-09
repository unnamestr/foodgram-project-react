from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, filters
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import Tag, Ingredient, Recipe, FavoriteRecipe, ShoppingCart
from users.models import User
from api.serializers import TagSerializer, IngredientSerializer, RecipeSerializer, FavoriteRecipeSerializer, \
    ShoppingCartSerializer, UserSerializer, PasswordSerializer, UserWithRecipeSerializer


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
    filter_backends = (DjangoFilterBackend,)
    #filterset_fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')


class FavoriteRecipeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, recipe_id):
        serializer = FavoriteRecipeSerializer(data={'user': request.user.id, 'recipe': recipe_id},
                                              context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user_id = request.user.id
        if not ShoppingCart.objects.filter(user=user_id, recipe=recipe_id).exists():
            return Response({"errors": "рецепта нет в списке покупок"}, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShoppingCart.objects.filter(user=user_id, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
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

    @action(detail=False, url_path='me', permission_classes=[IsAuthenticated])
    def user_me(self, request):
        serializer = self.serializer_class(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='set_password', permission_classes=[IsAuthenticated])
    def set_password(self, request):
        user = request.user
        serializer = PasswordSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'], url_path='subscribe', permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, id=pk)
        user = request.user
        if user == author:
            return Response({"detail": "Subscribe to myself"}, status=status.HTTP_400_BAD_REQUEST)
        if request.method == "POST":
            if user.is_following(author):
                return Response({"detail": "Already subscribed."}, status=status.HTTP_400_BAD_REQUEST)
            user.follow(author)
            recipes_limit = request.query_params.get('recipes_limit')
            serializer = UserWithRecipeSerializer(author, context={'request': request, 'recipes_limit': recipes_limit})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if not user.is_following(author):
            return Response({"detail": "Not subscribed."}, status=status.HTTP_400_BAD_REQUEST)
        user.unfollow(author)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, url_path='subscriptions', permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        recipes_limit = request.query_params.get('recipes_limit')
        serializer = UserWithRecipeSerializer(self.paginate_queryset(User.objects.filter(following__user=request.user)),
                                              many=True, context={"request": request, 'recipes_limit': recipes_limit})
        return self.get_paginated_response(serializer.data)
