# Register your models here.
from django.contrib import admin
from recipes.models import Ingredient, IngredientAndAmount, Category, AmountType

admin.site.register(Ingredient)
admin.site.register(IngredientAndAmount)
admin.site.register(AmountType)
admin.site.register(Category)
