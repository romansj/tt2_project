from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    #id automātiski tiek pievienots ar auto increments django
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    directions = models.TextField()
    amount = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    Category = models.CharField(max_length=100) #vai arī te liekam izvēli? #vajadzēs vēl vienu field
    cooking_time = models.DurationField()
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('recipes:post-detail', kwargs={'pk': self.pk})



