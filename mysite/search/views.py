from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.template.loader import render_to_string

from recipes.models import Post, Ingredient, Category


def index(request):
    return render(request, 'index.html')


def recipe_results(request):
    # todo pagaidam 2

    url_parameter = request.GET.get("q")
    url_parameter_cat = request.GET.get("cat")

    if url_parameter and not url_parameter_cat:
        recipes = Post.objects.filter(title__icontains=url_parameter)
    elif url_parameter_cat and not url_parameter:
        print(url_parameter_cat, int(url_parameter_cat))
        recipes = Post.objects.filter(category_new_id=int(url_parameter_cat))
    elif url_parameter and url_parameter_cat:
        criterion1 = Q(title__icontains=url_parameter)
        criterion2 = Q(category_new_id=int(url_parameter_cat))
        recipes = Post.objects.filter(criterion2 & criterion1)  # var ari '(title__icontains=url_parameter, category_new_id=int(url_parameter_cat)) ieks filter'
    else:
        recipes = Post.objects.all()

    categories = Category.objects.all()
    ingredients = Ingredient.objects.all()

    paginator = Paginator(recipes, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ctxt = {"recipes": recipes, "categories": categories, "ingredients": ingredients, 'page_obj': page_obj}

    if request.is_ajax():
        html = render_to_string(
            template_name="render_many_posts.html",
            context={"recipes": recipes, "page_obj": page_obj}
        )

        data_dict = {"html_from_view": html}
        print(html)

        return JsonResponse(data=data_dict, safe=False)

    return render(request, "results.html", context=ctxt)


def browse(request):
    recipes = Post.objects.all()
    categories = Category.objects.all()
    ingredients = Ingredient.objects.all()

    ctxt = {}
    ctxt["recipes"] = recipes
    ctxt["categories"] = categories
    ctxt["ingredients"] = ingredients

    return render(request, "browse.html", context=ctxt)
