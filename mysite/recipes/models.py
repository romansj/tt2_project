from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    subCategoryID = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:category-detail', kwargs={'pk': self.pk})


class Ingredient(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Post(models.Model):
    # id automātiski tiek pievienots ar auto increments django
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, blank=True)
    directions = RichTextUploadingField()
    amount = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                               blank=True)  # lietotajs tiek dzests, bet post paliek "by (deleted)"
    # Category = models.CharField(max_length=100)  # vai arī te liekam izvēli? #vajadzēs vēl vienu field
    category_new = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                     blank=True)  # dzesot kategoriju, post taja bridi nebus kategorija, bet post lai paliek
    cooking_time = models.DurationField()
    thumbnail = models.ImageField(upload_to='profile_pics', blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('recipes:post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    # def getRatings(self):
    #     return Rating.objects.filter(rating__author=self).distinct()


class Recipe_report(models.Model):
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reported_post = models.ForeignKey(Post, on_delete=models.CASCADE, default='0')
    reported_text = models.TextField()

    def __str__(self):
        return self.reported_user.username


class AmountType(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class IngredientAndAmount(models.Model):
    author = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField()
    amount_type = models.ForeignKey(AmountType, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.author and self.amount


class Rating(models.Model):
    stars = models.IntegerField()
    comment = models.TextField(max_length=1500)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    recipeID = models.ForeignKey(Post, on_delete=models.CASCADE)  # dzesot lietotaju, dzesas vina atsauksmes.
