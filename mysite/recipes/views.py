from django.views import generic

from .models import Post


# Create your views here.

class PostListView(generic.ListView):
    model = Post
    template_name = 'recipes/fresh.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(generic.DetailView):
    model = Post


class PostCreateView(generic.CreateView):
    model = Post
    fields = ['title', 'description', 'ingredients', 'directions', 'amount', 'Category', 'cooking_time']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
