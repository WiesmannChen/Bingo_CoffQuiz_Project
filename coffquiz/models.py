from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

class Coffee(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)
    picture = models.ImageField(upload_to='coffee_images', blank=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Coffee, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Coffee'

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)
    picture = models.ImageField(upload_to='article_images', blank=True)
    content = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar_images', blank=True)
    signature = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.user.username

class LikeCoffee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Like Coffee'

    def __str__(self):
        return self.user.username + 'likes' + self.coffee.name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username + 'comments' + self.article.title