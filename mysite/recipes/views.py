from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.core.mail import send_mail
from django.conf import settings
from .models import Post
from django.shortcuts import render


# Create your views here.

class PostListView(generic.ListView):
    model = Post
    template_name = 'recipes/fresh.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


def report(request):
    template_name = 'recipes/report.html'
    a = "zinojums"
    if request.method == 'POST':
        send_mail('Report', a, settings.EMAIL_HOST_USER, ['amachefDF@gmail.com'], fail_silently=False)
    return render(request, 'recipes/report.html')



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
