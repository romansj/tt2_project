from django.forms import ModelForm

from .models import Post


# class NewPostForm(forms.Form):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     ingredients = models.ManyToManyField(Ingredient, blank=True)
#     directions = models.TextField()
#     amount = models.IntegerField()
#     author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
#                                blank=True)  # lietotajs tiek dzests, bet post paliek "by (deleted)"
#     # Category = models.CharField(max_length=100)  # vai arī te liekam izvēli? #vajadzēs vēl vienu field
#     category_new = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
#                                      blank=True)  # dzesot kategoriju, post taja bridi nebus kategorija, bet post lai paliek
#     cooking_time = models.DurationField()
#     date_posted = models.DateTimeField(default=timezone.now)
#
#     class Meta:
#         model = Post
#         fields = ['title', 'description', 'ingredients', 'directions', 'amount', 'category_new', 'cooking_time']

class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'ingredients', 'directions', 'amount', 'category_new', 'cooking_time']
