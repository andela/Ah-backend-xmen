from rest_framework import generics, status, serializers
from authors.apps.articles.serializers import (
    ArticleSerializer, ArticleUpdateSerializer, ArticleRatingSerializer, 
    FavoriteSerializer, ReadStatsSerializer, BookmarksSerializer, ReportArticleSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from authors.apps.articles.renderers import ArticleJSONRenderer, FavortiesJsonRenderer
from django.shortcuts import get_object_or_404
from authors.apps.utils.custom_permissions.permissions import (
    check_if_is_author, can_report
)
from authors.apps.profiles.models import Profile
from rest_framework.response import Response
from authors.apps.articles.models import (
    Article, ArticleLikes, ArticleRating, ReadStats
)
from authors.apps.utils.messages import error_messages


class ArticleUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """ Updates and deletes an article instance """
    serializer_class = ArticleUpdateSerializer
    permission_class = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)

    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article, slug=slug)

    def perform_update(self, serializer):
        article = self.get_object()
        check_if_is_author(article, self.request)
        serializer.save(
            author=Profile.objects.get(user=self.request.user)
        )

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        check_if_is_author(instance, self.request)
        self.perform_destroy(instance)
        return Response(
            {"message": error_messages['delete_msg'].format('Article')},
            status=status.HTTP_200_OK)

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.format_kwarg = self.get_format_suffix(**kwargs)

        # checks for permissions
        self.perform_authentication(request)
        self.check_permissions(request)
        self.check_throttles(request)
        # Perform content negotiation and store the accepted info on the request
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        article = get_object_or_404(Article,slug=kwargs.get("slug"))
        if str(article.author) == str(request.user.username):
            return None
            
        try:
            if request.user.is_anonymous:
                return
            ReadStats.objects.filter(article=article).get(user=request.user)
        except ReadStats.DoesNotExist:
            article = get_object_or_404(Article, slug = kwargs.get("slug"))
            serializer = ReadStatsSerializer(data={})
            serializer.is_valid(raise_exception=True)
            serializer.save(user = request.user,article = article, read_stats=++1)
