from rest_framework.viewsets import ModelViewSet

from recipes.models import Tag, Ingredient
from .serializers import TagSerializer, IngredientSerializer
from rest_framework import filters

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)