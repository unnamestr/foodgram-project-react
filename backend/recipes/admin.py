from django.contrib import admin

from .models import Tag, Recipes, Ingredient

admin.site.register([Tag, Recipes, Ingredient])