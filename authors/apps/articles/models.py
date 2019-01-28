from django.db import models
from .utils import (
    generate_slug, unique_code_generator,
    get_likes_or_dislkes, get_average_value)
from django.core.mail import mail_admins
from django.db.models.signals import pre_save, post_save
from authors.apps.authentication.models import User 
from authors.apps.profiles.models import Profile
from authors.apps.utils.messages import error_messages, favorite_actions_messages

from authors.apps.authentication.models import User
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse


class ArticleManager(models.Manager):
    def handle_favorite_actions(self, request_user_obj, article_slug):
        """ 
        Enales both favoriting of articles 
        Args:
            request_user_obj:  Django http request user
            article_slug: Article model instance

        """
        profile_ = Profile.objects.filter(user=request_user_obj).first()
        article_ = self.model.objects.filter(slug=article_slug).first()
        article_.favoritesCount = article_.favorites.count() + 1
        article_.favorited = True
        article_.favorites.add(profile_)
        article_.save()
        return favorite_actions_messages.get('favorited')

    def handle_unfavorite(self, **kwargs):
        """ 
        Handles unfavoriting of articles 
        Args:
            request_user:  currently loggedin user
            article_slug: Article model instance

        """
        article_slug = kwargs.get("article_slug")
        request_user = kwargs.get("request_user")
        user_ = Profile.objects.get(user=request_user)
        article_to_unfavorite = self.model.objects.get(slug=article_slug)
        if article_to_unfavorite.favorites.count():
            article_to_unfavorite.favoritesCount = article_to_unfavorite.favorites.count() - 1
            article_to_unfavorite.favorites.remove(user_)
            article_to_unfavorite.favorited =  article_to_unfavorite.favorites.count() > 0
            article_to_unfavorite.save()
            return favorite_actions_messages.get('un_favorited')


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    favorites = models.ManyToManyField(Profile, related_name='favorited_articles', blank=True)
    favorited = models.BooleanField(default=False)
    favoritesCount = models.IntegerField(default=0)
    body = models.TextField()
    image = models.ImageField(upload_to='articles/images/', blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    objects = ArticleManager()

    tags = ArrayField(models.CharField(max_length=250), blank=True, default=list)
    read_stats = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('articles:article-update', kwargs={'slug': self.slug})

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


class ReportArticle(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reported_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    reason = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return f"{self.reported_article.title} reported by {self.reporter.username}"

    class Meta:
        ordering = ['-reported_at']
  
class ReadStats(models.Model):
    """ 
    This class is to hold data aquired from the statistics of the article 
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_stats = models.IntegerField(default=0)

    def __str__(self):
        return "article_title: {}, user: {}, read_stats: {}".format(
            self.article,
            self.user,
            self.read_stats)
