from django.urls import path

from .views import PostListView, PostDetailView, PostCreateView

app_name = 'recipes'

urlpatterns = [
    path('', PostListView.as_view(), name='fresh'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
]
