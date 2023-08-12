from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import (UserViewSet, TagViewSet, IngredientViewSet,
                    RecipeViewSet, FavoriteRecipeView, ShoppingCartView,
                    download_shopping_cart)

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
router.register('users', UserViewSet)


urlpatterns = [path('recipes/download_shopping_cart/', download_shopping_cart),
               path('', include(router.urls)),
               path('recipes/<int:recipe_id>/favorite/',
                    FavoriteRecipeView.as_view()),
               path('recipes/<int:recipe_id>/shopping_cart/',
                    ShoppingCartView.as_view()),
               ]
