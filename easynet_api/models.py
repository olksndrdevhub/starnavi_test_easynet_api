import re
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from datetime import date


class User(AbstractUser):
    last_request_time = models.CharField(verbose_name='last request time', max_length=100)


class Post(models.Model):

    """
    Model that describe Post objects
    """

    title = models.CharField(verbose_name='Post title', max_length=100)
    body = models.CharField(verbose_name='Post body', max_length=1000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Author', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_like', blank=True)
    created = models.DateField(verbose_name='Created', default=date.today)

    def __str__(self):
        return f'Post: {self.title}, created: {self.created}'

    def likes_count(self):
        return self.likes.count()

    @property
    def get_author(self):
        return self.author.id

    def like_post(self, user):
        self.likes.add(user)
        return self.likes_count()

    def unlike_post(self, user):
        self.likes.remove(user)
        return self.likes_count()
