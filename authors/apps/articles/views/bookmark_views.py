from rest_framework import generics, serializers
from authors.apps.articles.serializers import BookmarksSerializer
from rest_framework.permissions import IsAuthenticated
from authors.apps.articles.renderers import BookmarkJSONRenderer
from django.shortcuts import get_object_or_404
from authors.apps.articles.models import Article, Bookmark
from rest_framework.response import Response
from rest_framework import status


class BookmarkAPIView(generics.GenericAPIView):
    """ puts and deletes a bookmark """
    serializer_class = BookmarksSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (BookmarkJSONRenderer,)

    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def fetch_required_params(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        me = request.user.profile
        bookmarks = me.bookmarks.all()
        return article, me, bookmarks

    def post(self, request, slug):
        article, me, bookmarks = self.fetch_required_params(request, slug)
        for bookmark in bookmarks:
            if bookmark.article.slug == slug:
                raise serializers.ValidationError('Article already bookmarked')
        new_bookmark = Bookmark.objects.create(article=article, profile=me)
        return Response({'message': 'Article added to bookmarks'},
                        status=status.HTTP_200_OK)

    def delete(self, request, slug):
        article, me, bookmarks = self.fetch_required_params(request, slug)
        for bookmark in bookmarks:
            if bookmark.article.slug == slug:
                bookmark.delete()
                return Response({'message': 'Article removed from bookmarks'}, status=status.HTTP_200_OK)
        raise serializers.ValidationError('Article not in your bookmarks')


class BookmarksListView(generics.ListAPIView):
    serializer_class = BookmarksSerializer
    permission_classes = [IsAuthenticated, ]
    renderer_classes = [BookmarkJSONRenderer, ]

    def get_queryset(self):
        me = self.request.user.profile
        return me.bookmarks.all()
