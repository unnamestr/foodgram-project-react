from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import TagViewSet, IngredientViewSet

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [path('', include(router.urls)),]