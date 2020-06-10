from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.template.loader import render_to_string

from recipes.models import Post, Ingredient, Category


def index(request):
    return render(request, 'index.html')


def recipe_results(request):
    # todo pagaidam 2
    paginate_by = 2

    url_parameter = request.GET.get("q")

    if url_parameter:

        recipes = Post.objects.filter(title__icontains=url_parameter)
    else:
        recipes = Post.objects.all()

    categories = Category.objects.all()
    ingredients = Ingredient.objects.all()

    ctxt = {}
    ctxt["recipes"] = recipes
    ctxt["categories"] = categories
    ctxt["ingredients"] = ingredients

    if request.is_ajax():
        html = render_to_string(
            template_name="artists-results-partial.html",
            context={"recipes": recipes}
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
