import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from search.forms import RatingForm
from .forms import NewPostForm
from .models import Post, Category, Rating, Recipe_report


# Create your views here.

class PostListView(generic.ListView):
    # todo pagaidam 2
    paginate_by = 2
    model = Post
    template_name = 'recipes/fresh.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)

        top_posts = Post.objects.all().filter(is_hidden=False).order_by('rating__stars')
        paginator = Paginator(top_posts, 2)  # Show 25 contacts per page.
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context.update({
            'page_obj': page_obj,
            'top_posts': top_posts,
            # 'top_categories': Category.objects.all().annotate(num_submissions=Count('category_posts')).order_by('-num_submissions')[:7]
            'top_categories': Category.objects.all().annotate(num_submissions=Count('category_posts')).order_by('-num_submissions')[:7]
        })
        return context

    def get_queryset(self):
        return Post.objects.filter(is_hidden=False)


# def report(request):
#     template_name = 'recipes/report.html'
#     a = "zinojums"
#     if request.method == 'POST':
#         send_mail('Report', a, settings.EMAIL_HOST_USER, ['amachefDF@gmail.com'], fail_silently=False)
#     return render(request, 'recipes/report.html')


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

        context = {"rating": rating, "post": Post.objects.get(id=pk)}
        return render(request, "recipes/render_one_comment.html", context)

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
            return redirect('recipes:post-detail', pk=pk)
            response = JsonResponse({"success": "Rating deleted."})
            return response

    response = JsonResponse({"error": "Cannot delete recipe for some unknown reason"})
    response.status_code = 403  # To announce that the user isn't allowed to publish
    return redirect('recipes:post-detail', pk=pk)


def rating_edit(request, pk):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}

        # find rating
        # edit
        # return HttpResponse


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    # print("printeejas")
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
        if (self.request.user == post.author) or self.request.user.is_moderator:
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


class PostCopyView(LoginRequiredMixin, generic.CreateView):
    print("esam iekshaa postcopyview")
    model = Post
    form_class = NewPostForm
    success_url = '/post/%(id)s'

    def init_values(self, form):
        print("esam iekshaa init_values")
        post_text = self.request.POST.get('recid')
        post = Post.objects.get(id=int(post_text))
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.title = post.title
        obj.description = post.description
        obj.ingredients = post.ingredients
        obj.directions = post.directions
        obj.amount = post.amount
        obj.category_new = post.category_new
        obj.cooking_time = post.cooking_time
        obj.save()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def copy_post(request, pkk):
    print("esmu iekshaa def copy_post")
    new_item = get_object_or_404(Post, pk=pkk)
    new_item.pk = None
    new_item.author = request.user
    new_item.title = "Copy of " + new_item.title
    form = NewPostForm(request.POST or None, instance=new_item)
    if form.is_valid():
        form.save()
        return redirect('recipes:post-detail', pk=new_item.id)
    context = {
        "form": form,
    }
    return render(request, "recipes/post_form.html", context)


def hide_post(request, peekay):
    print("esmu iekshaa def hide_post")
    hide_item = get_object_or_404(Post, pk=peekay)
    hide_item.is_hidden = True
    hide_item.save()
    return redirect('recipes:post-detail', pk=hide_item.pk)


def Add_ingredient(request, pk):
    if request.method == 'POST':
        post_text = request.POST.get('the_ingredient_name')
        post_stars = request.POST.get('the_ingredient_amount')
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


def unhide_post(request, peekay):
    print("esmu iekshaa def hide_post")
    hide_item = get_object_or_404(Post, pk=peekay)
    hide_item.is_hidden = False
    hide_item.save()
    return redirect('recipes:post-detail', pk=hide_item.pk)


class HiddenRecipesView(generic.ListView):
    model = Post
    template_name = 'recipes/hidden_recipes.html'
    context_hidden_status = True
    paginate_by = 2
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_queryset(self):
        return Post.objects.filter(is_hidden=True)
