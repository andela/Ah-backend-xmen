from rest_framework import generics, status, serializers
from ..models import Article, ArticleLikes, Bookmark, ArticleRating
from django.core.mail import mail_admins
from django.shortcuts import get_object_or_404

from ..serializers import (
    ArticleSerializer, ArticleUpdateSerializer, BookmarksSerializer,
    ArticleRatingSerializer, FavoriteSerializer, ReportArticleSerializer
)
from authors.apps.articles.renderers import ArticleJSONRenderer, FavortiesJsonRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from authors.apps.utils.messages import error_messages, favorite_actions_messages, escalation_message
from authors.apps.profiles.models import Profile
from authors.apps.utils.custom_permissions.permissions import (
    check_if_is_author, can_report
)
from authors.apps.articles.paginators import ArticlePageNumberPagination
from authors.apps.articles.utils import get_like_status, get_usernames
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from authors.apps.articles.filters import ArticleFilter
from authors.apps.notifications.backends import notify


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_classes = (ArticleJSONRenderer,)
    permission_classes = (IsAuthenticated, )
    pagination_class = ArticlePageNumberPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('title', 'body', 'description', 'author__user__username')
    filter_class = ArticleFilter

    def perform_create(self, serializer):
        article = serializer.save(
            author=Profile.objects.get(user=self.request.user)
        )
        notify.article_created(self.request, article)

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]

        else:
            self.permission_classes = [IsAuthenticated, ]
        return super(ArticleListCreateView, self).get_permissions()


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
            notify.article_interaction_liked_or_faved(
                request, like.article, liked_by=like.user.profile
            )

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


class TagListAPIView(generics.ListAPIView):
    """ Create a view that is used to fetch all the tags """
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        tags_set = set()
        for article in Article.objects.all():
            for tag in article.tags:
                tags_set.add(tag)
        return Response({'tags': list(tags_set)}, status=status.HTTP_200_OK)


class RatingsAPIView(generics.GenericAPIView):
    serializer_class = ArticleRatingSerializer
    permission_classes = [IsAuthenticated, ]
    renderer_classes = [ArticleJSONRenderer, ]

    def post(self, request, slug):

        user = request.user
        score = request.data.get('rating')
        article = get_object_or_404(Article, slug=slug)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            ArticleRating.objects.get(
                user=user.pk,
                article_id=article.pk,
                rating=score
            )
            return Response(
                {"message": "You have already rated the article"},
                status=status.HTTP_200_OK)
        except ArticleRating.DoesNotExist:
            serializer.save(user=user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED) 


class FavoriteHandlerView(generics.GenericAPIView):
    serialiser_class = ArticleSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article, slug=slug)

    def post(self, *args, **kwargs):
        loggedin_user = self.request.user
        article = self.get_object()
        if article in loggedin_user.profile.favorited_articles.all():
            message = Response({"message":favorite_actions_messages.get('already_favorited')}, 
                               status=status.HTTP_400_BAD_REQUEST)
        else:
            message = Response({
            "message": Article.objects.handle_favorite_actions(
                request_user_obj=loggedin_user, article_slug=article.slug)
        }, status=status.HTTP_200_OK)
        notify.article_interaction_liked_or_faved(self.request,article,favorited_by=loggedin_user.profile)
        return message

    def delete(self, *args, **kwargs):
        loggedin_user = self.request.user
        article = self.get_object()
        if article in loggedin_user.profile.favorited_articles.all():
            return Response({
                "message": Article.objects.handle_unfavorite(
                    request_user=loggedin_user, article_slug=article.slug)
        }, status=status.HTTP_200_OK)
        else:
            return Response({"message": favorite_actions_messages.get('not_favorited')},
                            status=status.HTTP_400_BAD_REQUEST)  


class FavoritesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [FavortiesJsonRenderer, ]
    serializer_class = FavoriteSerializer

    def get_queryset(self, *args, **kwargs):
        my_profile = self.request.user.profile
        return my_profile.favorited_articles.all()


class ReportArticleView(generics.CreateAPIView):
    """ Escalate an article for review """
    permission_classes = [IsAuthenticated, ]
    serializer_class = ReportArticleSerializer

    def get_object(self):
        article_slug = self.kwargs.get("slug")
        return get_object_or_404(Article, slug=article_slug)
    
    def post(self, *args, **kwargs):
        data = self.request.data
        data['reporter'] = self.request.user.pk
        data['reported_article'] = self.get_object().pk
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        
        formatted_mail = escalation_message.format(
            self.request.user.username,
            self.request.build_absolute_uri(self.get_object().get_absolute_url()),
            data.get('reason')
        )
        can_report(self.get_object(), self.request.user.profile)
        serializer.save()
        mail_admins(subject='Attention required!', message=formatted_mail)

        
        return Response({
                "message":"Article successfully reported, article will be reviewed.",    
        }, status=status.HTTP_201_CREATED)
