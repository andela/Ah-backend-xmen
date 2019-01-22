from django.db import models
from .utils import (
    generate_slug, unique_code_generator,
    get_likes_or_dislkes, get_average_value)
from django.db.models.signals import pre_save
from authors.apps.profiles.models import Profile
from authors.apps.authentication.models import User


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    favorited = models.BooleanField(default=False)
    favoritesCount = models.IntegerField(default=0)
    body = models.TextField()
    image = models.ImageField(upload_to='articles/images/', blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    @property
    def likes_count(self):
        return get_likes_or_dislkes(
            model=ArticleLikes,
            like_article=True,
            article_id=self.pk
        )

    @property
    def dislikes_count(self):
        return get_likes_or_dislkes(
            model=ArticleLikes,
            like_article=False,
            article_id=self.pk
        )

    @property
    def average_rating(self):
        return get_average_value(
            model=ArticleRating,
            article_id=self.pk,
            rating=ArticleRating.rating
        )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


def article_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_slug(instance) + "-" + unique_code_generator()


pre_save.connect(article_pre_save_receiver, Article)


class ArticleLikes(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE,
        null=True, related_name="article_likes", blank=True)
    like_article = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Bookmark(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='is_bookmarked')
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='bookmarks')


class ArticleRating(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE,
        null=True, related_name='article_ratings', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
