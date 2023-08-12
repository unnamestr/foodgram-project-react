from django.contrib import admin

from .models import Tag, Recipe, Ingredient, IngredientInRecipe, FavoriteRecipe, ShoppingCart

class IngredientInRecipeInline(admin.StackedInline):
    model = IngredientInRecipe
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInRecipeInline, )
    list_filter = ('author', 'name', 'tags',)
    search_fields = ('name',)
    list_display = ('id', 'name', 'author', 'in_favorites',)

    def in_favorites(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj).count()

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name', )
    search_fields = ('name', )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register([Tag, FavoriteRecipe, ShoppingCart])