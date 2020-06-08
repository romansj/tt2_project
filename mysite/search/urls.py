from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='search'),
    path('results/', views.recipe_results, name='results'),
]
