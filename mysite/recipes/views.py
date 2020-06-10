from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'description', 'ingredients', 'directions', 'amount', 'category_new', 'cooking_time']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'description', 'ingredients', 'directions', 'amount', 'category_new', 'cooking_time']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    success_url = '/recipes'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostCopyView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'description', 'ingredients', 'directions', 'amount', 'category_new', 'cooking_time']
    # def get_absolute_url(self):
    #    return "/post/%i/" % self.id
    # idintegers = get_absolute_url(Post.objects.self)
    # mystring = "text"
    # mystring = str(id)
    # idintegers = int(mystring)
    # id_paraneter = Post.objects.get()
    # def get(self, request, **kwargs):
    # copied_post.pk = None
    # copied_post.id = None
    copied_post = Post.objects.get(pk=7)
    # def values(self, request, **kwargs):
    #    copied_post = Post.objects.get(pk=self.kwargs.get('pk'))
    #
    #       fields = ['title', 'description', 'ingredients', 'directions', 'amount', 'category_new', 'cooking_time']
    #      initial = {'title': copytitle, 'description': copydesc, 'directions': copydirec, 'amount': copyamount,
    #                'category_new': copycat, 'cooking_time': copytime}
    #    return super().values(self)

    copytitle = copied_post.title
    copydesc = copied_post.description
    # copyingr = copied_post.ingredients
    copydirec = copied_post.directions
    copyamount = copied_post.amount
    copycat = copied_post.category_new
    copytime = copied_post.cooking_time
    initial = {'title': copytitle, 'description': copydesc, 'directions': copydirec, 'amount': copyamount,
               'category_new': copycat, 'cooking_time': copytime}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
