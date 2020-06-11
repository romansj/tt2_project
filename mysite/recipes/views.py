import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.views import generic

from search.forms import RatingForm
from .models import Post, Category, Rating, Recipe_report


# Create your views here.

class PostListView(generic.ListView):
    # todo pagaidam 2
    paginate_by = 2
    model = Post
    template_name = 'recipes/fresh.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = RatingForm()
        context['form'] = form
        return context


def report(request, pk):
    response_data = {}
    model = Recipe_report
    if request.method == 'POST':
        report_text = request.POST.get('the_report')
        response_data['author'] = request.user.username
        response_data['text'] = report_text
        response_data['postpk'] = pk
        print(request.user.username)
        # šī daļa ir tur kur strādā liekot datu
        reporting = Recipe_report(reported_user=request.user, reported_post=Post.objects.get(id=pk),
                                  reported_text=report_text)
        reporting.save()
        text = request.user.username + report_text + str(pk)
        send_mail('Report', text, settings.EMAIL_HOST_USER, ['amachefDF@gmail.com'], fail_silently=False)
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


def post_rating(request, pk):
    # ratingForThisRecipe = Rating.objects.filter(author__rating__recipeID=pk).distinct()
    ratingForThisRecipe = Rating.objects.filter(author_id=request.user.id, author__rating__recipeID=pk)

    if (ratingForThisRecipe):
        response = JsonResponse({"error": "You have already rated this recipe."})
        response.status_code = 403  # To announce that the user isn't allowed to publish
        return response

    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        post_stars = request.POST.get('the_stars')
        response_data = {}

        rating = Rating(stars=post_stars, comment=post_text, author=request.user, recipeID_id=pk)
        rating.save()

        response_data['postpk'] = pk
        response_data['result'] = 'Create post successful!'
        response_data['ratingpk'] = rating.pk
        response_data['comment'] = rating.comment
        response_data['author'] = rating.author.username
        response_data['stars'] = rating.stars

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def rating_delete(request, pk, rpk):
    if request.method == 'GET':
        # delete = request.GET.get('the_delete')
        # if (delete):

        rating = Rating.objects.filter(id=rpk)
        if rating:
            print('rating exists, deleting')
            rating.delete()

            response = JsonResponse({"success": "Rating deleted."})
            return response

    response = JsonResponse({"error": "Cannot delete recipe for some unknown reason"})
    response.status_code = 403  # To announce that the user isn't allowed to publish
    return response


def rating_edit(request, pk):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}

        # find rating
        # edit
        # return HttpResponse


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'description', 'ingredients', 'directions', 'amount', 'category_new', 'cooking_time',
              'thumbnail']

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

    # important, tests if the user is author, if he can actually delete
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CategoryListView(generic.ListView):
    # todo pagaidam 2
    paginate_by = 2
    model = Category
    template_name = 'recipes/categories.html'
    context_object_name = 'categories'


class CategoryDetailView(generic.DetailView):
    model = Category

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     recipes = Post.objects.filter(categ)
    #     context["recipes"] = recipes
    #     return context

# class PostCopyView(LoginRequiredMixin, generic.CreateView):
#     model = Post
#     fields = ['title', 'description', 'ingredients', 'directions', 'amount', 'category_new', 'cooking_time']
#     # def get_absolute_url(self):
#     #    return "/post/%i/" % self.id
#     # idintegers = get_absolute_url(Post.objects.self)
#     # mystring = "text"
#     # mystring = str(id)
#     # idintegers = int(mystring)
#     # id_paraneter = Post.objects.get()
#     # def get(self, request, **kwargs):
#     # copied_post.pk = None
#     # copied_post.id = None
#     copied_post = Post.objects.get(pk=7)
#     # def values(self, request, **kwargs):
#     #    copied_post = Post.objects.get(pk=self.kwargs.get('pk'))
#     #
#     #       fields = ['title', 'description', 'ingredients', 'directions', 'amount', 'category_new', 'cooking_time']
#     #      initial = {'title': copytitle, 'description': copydesc, 'directions': copydirec, 'amount': copyamount,
#     #                'category_new': copycat, 'cooking_time': copytime}
#     #    return super().values(self)
#
#     copytitle = copied_post.title
#     copydesc = copied_post.description
#     # copyingr = copied_post.ingredients
#     copydirec = copied_post.directions
#     copyamount = copied_post.amount
#     copycat = copied_post.category_new
#     copytime = copied_post.cooking_time
#     initial = {'title': copytitle, 'description': copydesc, 'directions': copydirec, 'amount': copyamount,
#                'category_new': copycat, 'cooking_time': copytime}
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
