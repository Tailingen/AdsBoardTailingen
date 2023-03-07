from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through = 'SubscribersUsers')

    def __str__(self):
        return self.name

class SubscribersUsers(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    time_in = models.DateField(auto_now_add=True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length=100)
    text = models.TextField()

    def get_absolute_url(self):
        return reverse('ads_detail', args=[str(self.id)])

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)

