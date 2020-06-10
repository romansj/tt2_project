from django.urls import path

from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,report

app_name = 'recipes'

urlpatterns = [
    path('', PostListView.as_view(), name='fresh'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/report', views.report, name='report'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
