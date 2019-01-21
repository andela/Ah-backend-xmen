from django.db import models
from .utils import generate_slug, unique_code_generator
from django.db.models.signals import pre_save
from authors.apps.profiles.models import Profile


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

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


def article_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_slug(instance) + "-" + unique_code_generator()


pre_save.connect(article_pre_save_receiver, Article)
