import os
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime, timedelta, timezone

# Create your models here.
# class Category(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return f'/blog/category/{self.slug}'
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/community/tag/{self.slug}/'

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    # file_upload = models.FileField(upload_to='community/files/%Y/%m/%d', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'({self.pk}) {self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/community/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='community/images/%Y/%m/%d', blank=True, null=True)

