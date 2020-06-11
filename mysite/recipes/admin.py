# Register your models here.
from django.contrib import admin

from recipes.models import Ingredient, Category, Rating, Recipe_report

admin.site.register(Recipe_report)
admin.site.register(Ingredient)
admin.site.register(Category)
admin.site.register(Rating)
