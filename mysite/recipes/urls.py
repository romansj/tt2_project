from django.urls import path

from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CategoryListView, \
    CategoryDetailView, IngredientDetailView

app_name = 'recipes'

urlpatterns = [
    path('', PostListView.as_view(), name='fresh'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # TODO ELVIS
    path('post/report', views.report, name='report'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pkk>/copy/', views.copy_post, name='post-copy'),

    # path('post/<int:pk>/rate/', PostRateView.as_view(), name='post-rate'),

    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('post/<int:pk>/report/', views.report, name='report'),
    path('post/<int:pk>/rate/', views.post_rating, name='rate'),
    path('post/<int:pk>/rate/<int:rpk>/rating_delete/', views.rating_delete, name='rating_delete'),
    path('post/<int:pk>/rate/<int:rpk>/edit/', views.rating_edit, name='rating_edit'),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='ingredient_detail'),
]
