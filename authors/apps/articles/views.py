from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Article, ArticleLikes
from django.shortcuts import get_object_or_404
from .serializers import ArticleSerializer, ArticleUpdateSerializer
from .renderers import ArticleJSONRenderer
from rest_framework import status, serializers
from rest_framework.response import Response
from authors.apps.utils.messages import error_messages
from authors.apps.profiles.models import Profile
from authors.apps.utils.custom_permissions.permissions import (
    check_if_is_author,
)
from .paginators import ArticleLimitOffSetPagination
from .utils import get_like_status, get_usernames
from rest_framework.exceptions import NotFound


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    pagination_class = ArticleLimitOffSetPagination

    def perform_create(self, serializer):
        serializer.save(
            author=Profile.objects.get(user=self.request.user)
        )


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


class ArticleLikesView(generics.RetrieveUpdateDestroyAPIView):
    """Updates, retrieves and deletes an articlelikes instance"""
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)

    def put(self, request, slug):
        """
        Updates the article with the reader's feedback

        args:
            request (Request object): Django Request context
            slug (Article label): stores and generates a valid URL for the
                                    article.

        Returns:
            HTTP Response message: A dictionary
            HTTP Status code: 201, 200
        """

        user = request.user
        article_id = get_object_or_404(Article, slug=slug)
        like_article = request.data.get('like_article', None)

        if like_article is None:
            raise serializers.ValidationError(
                'like_article field is required')

        if type(like_article) != bool:
            raise serializers.ValidationError(
                'Value of like_article should be a boolean')

        try:
            like = ArticleLikes.objects.get(
                user=user, article=article_id, like_article=like_article)

            verb = get_like_status(like_article, 'liked', 'disliked')
            return Response(
                {'message': 'You have already {} the article'.
                    format(verb)},
                status=status.HTTP_200_OK)
        except ArticleLikes.DoesNotExist:
            like = ArticleLikes.objects.create(
                user=user, article=article_id, like_article=like_article)
            like.save()

            if ArticleLikes.objects.filter(
                user=user,
                article=article_id
            ).count() > 1:
                first_like = ArticleLikes.objects.get(
                    user=user,
                    article=article_id,
                    like_article=not like_article
                )
                first_like.delete()

            verb = get_like_status(like_article, 'liked', 'disliked')
            return Response(
                {'message': 'You have {} an article'.format(verb)},
                status=status.HTTP_201_CREATED)

    def delete(self, request, slug):
        """
        Removes the reader's feedback on the article

        args:
            request (Request object): Django Request context
            slug (Article label): stores and generates a valid URL for the
                                    article.

        Returns:
            HTTP Response message
            HTTP Status code: 200
        """

        user = request.user
        article_id = get_object_or_404(Article, slug=slug)

        try:
            like_ = ArticleLikes.objects.get(
                user=user, article=article_id)
            like_article = ArticleLikes.objects.filter(
                user=user,
                article=article_id
            ).values('like_article')[0].get('like_article')
            like_.delete()
            verb = get_like_status(like_article, 'unliked', 'un-disliked')
            return Response(
                {'message': 'You have {} an article'.
                    format(verb)},
                status=status.HTTP_200_OK)
        except ArticleLikes.DoesNotExist:
            raise serializers.ValidationError(
                "There is no like or dislike to remove")

    def get(self, request, slug):
        """
        Fetches a list of readers that gave feedback to an article

        args:
            request (Request object): Django Request context
            slug (Article label): stores and generates a valid URL for the
                                    article.

        Returns:
            HTTP Response message
            HTTP Status code: 200
        """

        article_id = get_object_or_404(Article, slug=slug)

        pleasured_users = get_usernames(
            model=ArticleLikes,
            article_id=article_id,
            like_article=True
        )
        displeasured_users = get_usernames(
            model=ArticleLikes,
            article_id=article_id,
            like_article=False
        )
        return Response(
            {'likes': pleasured_users,
                'dislikes': displeasured_users},
            status=status.HTTP_200_OK)
