import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from search.forms import RatingForm
from .forms import NewPostForm
from .models import Post, Category, Rating, Recipe_report, Ingredient


# Create your views here.

class PostListView(generic.ListView):
    # todo pagaidam 2
    paginate_by = 2
    model = Post
    template_name = 'recipes/fresh.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


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
        reporting = Recipe_report(reported_user=request.user, reported_post=Post.objects.get(id=pk), reported_text=report_text)
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
    # print("printeejas")
    model = Post
    fields = ['title', 'description', 'ingredients', 'directions', 'amount', 'category_new', 'cooking_time',
              'thumbnail']

    # def get_initial(self):
    #     print("esam get_initial")
    #     post_text = self.request.POST.get('recid')
    #     post = Post.objects.get(id=int(post_text))
    #     return {'title': post.title, 'description': post.description, 'directions': post.description,
    #             'amount': post.amount,
    #             'category_new': post.category_new, 'cooking_time': post.cooking_time}

    # def __init__(self, *args, **kwargs):
    #     print("ieeju def init ar baigaam sviitraam")
    #     post_text = self.request.POST.get('recid')
    #     post = Post.objects.get(id=int(post_text))
    #     super(PostCreateView, self).__init__(*args, **kwargs)
    #     self.
    #     self.fields['title'].initial = post.title
    #     self.fields['description'].initial = post.description
    #     self.fields['directions'].initial = post.directions
    #     self.fields['amount'].initial = post.amount
    #     self.fields['category_new'].initial = post.category_new
    #     self.fields['cooking_time'].initial = post.cooking_time

    def form_valid(self, form):
        print("shis arii printeejas")
        # if self.request.method == 'POST':
        #     post_text = self.request.POST.get('recid')
        #     response_data = {}
        #     post = Post.objects.get(id=int(post_text))
        #     form['title'] = post.title
        #     form['description'] = post.description
        #     form['directions'] = post.directions
        #     form['amount'] = post.amount
        #     form['category_new'] = post.category_new
        #     form['cooking_time'] = post.cooking_time
        # else:
        #     print("nav post bet gan ir ", self.request.method)

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
#     copied_post = Post.objects.get(pk=2)
#     copied_post.pk = None
#     copied_post.id = None
#     initiala = {}
#
#     def values(self, request, **kwargs):
#         copied_post = Post.objects.get(pk=self.kwargs.get('pk'))
#         copytitle = copied_post.title
#         copydesc = copied_post.description
#         copyingr = copied_post.ingredients
#         copydirec = copied_post.directions
#         copyamount = copied_post.amount
#         copycat = copied_post.category_new
#         copytime = copied_post.cooking_time
#         fields = ['title', 'description', 'ingredients', 'directions', 'amount', 'category_new', 'cooking_time']
#         initiala = {'title': copytitle, 'description': copydesc, 'directions': copydirec, 'amount': copyamount,
#                    'category_new': copycat, 'cooking_time': copytime}
#         return initiala
#
#
#     copytitle = copied_post.title
#     copydesc = copied_post.description
#     copyingr = copied_post.ingredients
#     copydirec = copied_post.directions
#     copyamount = copied_post.amount
#     copycat = copied_post.category_new
#     copytime = copied_post.cooking_time
#     initial = initiala
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

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
        # context = {
        #     "form": form,
        # }
        # return render(request, "recipes/post_form.html", context)
    context = {
        "form": form,
    }
    return render(request, "recipes/post_form.html", context)


# @moderator_required
# def hide_recipe():


class IngredientDetailView(generic.DetailView):
    model = Ingredient

# todo data_insertion
# def insert_data(request):
#     category = Category( "Breakfast and brunch","For all your breakfast and brunch needs")
#
#     words = ["Fluffy and Delicious Pancakes",
#              "Puff Pastry Waffles",
#              "Mom's Zucchini Bread",
#              "Fluffy French Toast",
#              "Strawberry Waffles",
#              "French Toast",
#              "Sausage Balls"]
#     descriptions = [
#         "My husband makes the most fabulous pancakes I've ever eaten! Well worth the hour wait! We serve them with butter and brown sugar.",
#         "Add puff pastry to the list of good things you can snackify in your waffle iron. Although they don't puff up as much as oven-baked puff pastry, they turn out crispy on the outside and tender on the inside, and they take only minutes to make. Serve hot or at room temperature with syrup, fruit, Nutella®, fruit preserves, or nut butter.",
#         "Really, really good and moist- my kids eat it as quickly as I can make it. Bread will freeze well, and keep in refrigerator for weeks.",
#         "This French toast recipe is different because it uses flour. I have given it to some friends and they've all liked it better than the French toast they usually make!",
#         "A rather quick and easy waffle recipe, with the added goodness of fresh strawberries. Serve warm, topped with warm maple syrup, or the fruit syrup of your choice.",
#         "There are many, fancy variations on this basic recipe. This recipe works with many types of bread - white, whole wheat, cinnamon-raisin, Italian or French. Serve hot with butter or margarine and maple syrup.",
#         "These are so yummy! My family makes every Christmas morning. Enjoy!"
#     ]
#     directions = [
#         "Step 1:\nIn a large bowl, sift together flour, salt, baking powder and sugar. In a small bowl, beat together egg and milk. Stir milk and egg into flour mixture. Mix in the butter and fold in the blueberries. Set aside for 1 hour. \n\n Step 2: \n Heat a lightly oiled griddle or frying pan over medium high heat. Pour or scoop the batter onto the griddle, using approximately 1/4 cup for each pancake. Brown on both sides and serve hot.",
#         "Step 1:\nLine a cutting board with parchment paper. Unfold puff pastry onto cutting board. Cut each sheet into 4 equal squares.\n\nStep 2\nPreheat a waffle iron according to manufacturer's instructions. Grease with cooking spray.\n\nStep 3\nPlace one puff pastry square in the preheated waffle iron; cook until golden brown, 3 to 5 minutes. Repeat with remaining puff pastry squares.",
#         "Step 1:\nGrease and flour two 8 x 4 inch pans. Preheat oven to 325 degrees F (165 degrees C).\n\nStep 2\nSift flour, salt, baking powder, soda, and cinnamon together in a bowl.\n\nStep 3\nBeat eggs, oil, vanilla, and sugar together in a large bowl. Add sifted ingredients to the creamed mixture, and beat well. Stir in zucchini and nuts until well combined. Pour batter into prepared pans.\n\nStep 4\nBake for 40 to 60 minutes, or until tester inserted in the center comes out clean. Cool in pan on rack for 20 minutes. Remove bread from pan, and completely cool.",
#         "Step 1\nMeasure flour into a large mixing bowl. Slowly whisk in the milk. Whisk in the salt, eggs, cinnamon, vanilla extract and sugar until smooth.\n\nStep 2\nHeat a lightly oiled griddle or frying pan over medium heat.\n\nStep 3\nSoak bread slices in mixture until saturated. Cook bread on each side until golden brown. Serve hot.",
#         "Step 1\nPreheat and grease a waffle iron according to manufacturer's instructions.\n\nStep 2\nSift flour, baking powder, and salt together in a bowl. Whisk buttermilk, yogurt, butter, eggs, and sugar together in a separate bowl; stir into flour mixture until batter is smooth. Fold strawberries into batter.\n\nStep 3\nPour about 1/3 cup batter into preheated waffle iron; cook until lightly browned, 5 to 7 minutes. Repeat with remaining batter.",
#         "Step 1\nBeat together egg, milk, salt, desired spices and vanilla.\n\nStep 2\nHeat a lightly oiled griddle or skillet over medium-high heat.\n\nStep 3\nDunk each slice of bread in egg mixture, soaking both sides. Place in pan, and cook on both sides until golden. Serve hot.",
#         "Step 1\nPreheat oven to 350 degrees F (175 degrees C).\n\nStep 2\nIn a large bowl, combine sausage, biscuit baking mix and cheese. Form into walnut size balls and place on baking sheets.\n\nStep 3\nBake in preheated oven for 20 to 25 minutes, until golden brown and sausage is cooked through.",
#     ]
#
#     ingredients = [
#         "¾ cup milk\n2 tablespoons white vinegar\n1 cup all-purpose flour\n2 tablespoons white sugar\n1 teaspoon baking powder\n½ teaspoon baking soda\n½ teaspoon salt\n1 egg\n2 tablespoons butter, melted\n1 ½ teaspoons ground cinnamon, or as desired\n1 teaspoon vanilla extract\n1 serving cooking spray\n",
#         "1 (17.3 ounce) package frozen puff pastry, thawed\n1 serving cooking spray",
#         "3 cups all-purpose flour\n1 teaspoon salt\n1 teaspoon baking soda\n1 teaspoon baking powder\n1 tablespoon ground cinnamon\n3 eggs\n1 cup vegetable oil\n2 ¼ cups white sugar\n3 teaspoons vanilla extract\n2 cups grated zucchini\n1 cup chopped walnuts\n",
#         "¼ cup all-purpose flour\n1 cup milk\n1 pinch salt\n3 eggs\n½ teaspoon ground cinnamon\n1 teaspoon vanilla extract\n1 tablespoon white sugar\n12 thick slices bread\n",
#    "2 ½ cups all-purpose flour\n4 teaspoons baking powder\n¾ teaspoon salt\n2 cups buttermilk\n½ cup vanilla Greek-style yogurt\n½ cup butter, melted\n2 eggs, beaten\n1 ½ tablespoons white sugar\n¾ cup chopped strawberries, or more to taste\n",
#     "6 thick slices bread\n2 eggs\n⅔ cup milk\n¼ teaspoon ground cinnamon\n¼ teaspoon ground nutmeg\n1 teaspoon vanilla extract\nsalt to taste\n",
#     "1 pound ground pork sausage\n2 cups biscuit baking mix\n1 pound sharp Cheddar cheese, shredded\n",]
#
#     count = 0
#     for word in words:
#         post = Post(word, descriptions[count], ingredients[count],directions[count],1,request.user,category,'02:30:00','',timezone.now, False)
#         count+=1
