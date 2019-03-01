from rest_framework import serializers
from .models import (
    Article, ArticleLikes, Bookmark, ArticleRating, 
    ReportArticle, ReadStats
)
from rest_framework.exceptions import NotFound
from ..authentication.models import User
from authors.apps.profiles.models import Profile
from authors.apps.profiles.serializers import UserProfileSerializer
from authors.apps.utils.estimator import article_read_time
from authors.apps.utils.share_links import share_links_generator
from authors.apps.utils.user_rated import get_user_rated

from authors.apps.authentication.models import User


class AuthorProfileSerializer(UserProfileSerializer):

    class Meta:
        model = Profile
        fields = ('bio', 'username', 'image', 'following', )


class ArticleSerializer(serializers.ModelSerializer):

    author = AuthorProfileSerializer(read_only=True)
    read_time = serializers.SerializerMethodField()
    share_links = serializers.SerializerMethodField()
    favorites = serializers.SerializerMethodField()
    read_stats = serializers.SerializerMethodField()
    user_rated=serializers.SerializerMethodField()

    """ 
    Add the field required in the database so as to hold
    data from user add a tags field for the tags
    that a user is going to append to their article
    """
    class Meta:
        model = Article
        fields = ('title', 'slug', 'description', 'created_at',
                  'updated_at', 'favorited', 'favorites', 'favoritesCount',
                  'body', 'image', 'author', 'read_time', 'share_links',
                  'likes_count', 'dislikes_count', 'average_rating', 'read_stats', 
                  'tags','user_rated')

    def generate_usernames(self, profiles):
        """
        Args:
           profiles: Django model queryset
        Yields:
           string: username mapping to user profile id
        """
        for profile in profiles:
                yield profile.user.username

    def get_favorites(self, obj):
        return list(self.generate_usernames(
            obj.favorites.all()
            ))

    def get_read_time(self, obj):
        return article_read_time(obj.body)

    def get_share_links(self, obj):
        return share_links_generator(obj, self.context['request'])

    def get_read_stats(self, obj):
        return ReadStats.objects.filter(article=obj).count()

    def get_user_rated(self,obj):
        return get_user_rated(self, obj)


class ArticleUpdateSerializer(serializers.ModelSerializer):
    author = AuthorProfileSerializer(read_only=True)
    read_time = serializers.SerializerMethodField()
    share_links = serializers.SerializerMethodField()  
    read_stats = serializers.SerializerMethodField()
    user_rated=serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = [
            'title',
            'description',
            'body',
            'created_at',
            'updated_at',
            'favorited',
            'favorites',
            'favoritesCount',
            'image',
            'author',
            'read_time',
            'share_links',
            'likes_count',
            'dislikes_count',
            'read_stats',
            'average_rating',
            'tags',
            'user_rated'
        ]

    def get_read_time(self, obj):
        return article_read_time(obj.body)

    def get_share_links(self, obj):
        return share_links_generator(obj, self.context['request'])
    
    def get_read_stats(self, obj):
        return ReadStats.objects.filter(article=obj).count()

    def get_user_rated(self,obj):
        return get_user_rated(self, obj)


class BookmarksSerializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    author = AuthorProfileSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ('title', 'slug', 'description', 'author')

    def get_title(self, obj):
        return obj.article.title

    def get_slug(self, obj):
        return obj.article.slug

    def get_description(self, obj):
        return obj.article.description


class ArticleRatingSerializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    rating = serializers.IntegerField(required=True, max_value=5, min_value=0)

    class Meta:
        model = ArticleRating
        fields = ('title', 'author', 'rating')

    def get_title(self, obj):
        return obj.article.title

    def get_author(self, obj):
        return obj.article.author.user.username


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'title',
            'slug',
            'body',
        ]


class ReportArticleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReportArticle
        fields = [
            'reporter',
            'reported_article',
            'reason'
        ]


class ReadStatsSerializer(serializers.ModelSerializer):
    """
    This serializer is to handle the data from the ReadStats models
    """
    class Meta:
        model = ReadStats
        fields = ('user',
                  'article',
                  'read_stats'
                 )
        read_only_fields = ("user", "article")
