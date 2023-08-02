from django.contrib import admin

from .models import Tag, Recipe, Ingredient, IngredientInRecipe, FavoriteRecipe

class IngredientInRecipeInline(admin.StackedInline):
    model = IngredientInRecipe
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInRecipeInline]

admin.site.register(Recipe,RecipeAdmin)
admin.site.register([Tag, Ingredient, FavoriteRecipe])