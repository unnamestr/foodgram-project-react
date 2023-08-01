from django.contrib import admin

from .models import Tag, Recipe, Ingredient, CountIngredient

class CountIngredientInline(admin.StackedInline):
    model = CountIngredient
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = [CountIngredientInline]

admin.site.register(Recipe,RecipeAdmin)
admin.site.register([Tag, Ingredient])