from django.db import models

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    body = RichTextField(blank = True, null =True)
    date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,)
    likes = models.ManyToManyField(get_user_model(), related_name='article_articles')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail',args=[str(self.id)])
    def number_of_likes(self):
    	return self.likes.count()