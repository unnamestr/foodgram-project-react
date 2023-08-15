from django_filters.rest_framework.filters import (ModelChoiceFilter,
                                                   ModelMultipleChoiceFilter,
                                                   BooleanFilter, CharFilter)
from django_filters.rest_framework import FilterSet

from users.models import User
from recipes.models import Recipe, Tag, Ingredient


class RecipeFilter(FilterSet):
    """Фильтр для рецептов."""
    author = ModelChoiceFilter(queryset=User.objects.all())
    tags = ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
                                     field_name='tags__slug',
                                     to_field_name='slug')
    is_favorited = BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def filter_is_favorited(self, queryset, name, value):
        return self.filter_related(queryset, self.request.user.favorite, value)

    def filter_related(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            recipe = name.values_list('recipe', flat=True)
            return queryset.filter(id__in=recipe)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return self.filter_related(queryset, self.request.user.shopping_cart,
                                   value)


class IngredientFilter(FilterSet):
    """Фильтр для ингридиентов"""
    name = CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Ingredient
        fields = ('name',)
