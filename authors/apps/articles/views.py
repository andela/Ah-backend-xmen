from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Article
from django.shortcuts import get_object_or_404
from .serializers import ArticleSerializer, ArticleUpdateSerializer
from .renderers import ArticleJSONRenderer
from rest_framework import status
from rest_framework.response import Response
from authors.apps.utils.messages import error_messages
from authors.apps.profiles.models import Profile
from authors.apps.utils.custom_permissions.permissions import (
    check_if_is_author,
)
from .paginators import ArticleLimitOffSetPagination


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
