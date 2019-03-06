from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,   
    IsAuthenticated )
from rest_framework.response import Response
from authors.apps.articles.models import Article
from authors.apps.profiles.models import Profile
from .utils import update_obj
from authors.apps.utils.validators.validation_helpers import validate_index
from .serializers import (
    CommentSerializer, CommentLikeSerializer, CommentHistorySerailizer)
from .models import Comment, CommentLike
from authors.apps.utils.custom_permissions.permissions import (
    check_if_is_author, check_if_can_track_history)
from .renderers import CommentJSONRenderer
from authors.apps.notifications.backends import notify


class CommentView(GenericAPIView):
    """
    Allows authenticated users to post a comment on an
    articles
    and also view all comments on an article
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer

    def post(self, request, slug):
        """
        Allows authenticated users can add comments on articles

        Args:
            slug: this a slug for a particular article
        Returns:
            code: The return 201 created for success

        """
        self.author = get_object_or_404(Profile, user=request.user)
        self.article = get_object_or_404(Article, slug=slug)
        start_index = validate_index(request.data.get('highlight_start'), slug)
        end_index = validate_index(request.data.get('highlight_end'), slug)
        if start_index and end_index:
            selection = [int(start_index), int(end_index)] \
                if int(start_index) < int(end_index) \
                else [int(end_index), int(start_index)]
            highlight_text = str(self.article.body[selection[0]:selection[1]])
            request.data['highlight_text'] = highlight_text
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(author=self.author,article=self.article)
        notify.article_interaction_comment(request,comment)
        return Response({
            'comment': serializer.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request, slug):
        """
        get all comments on an article

        Args:
            param1 (slug): this a slug for a particular article
        Returns:
            code: The return 201 created for success
        """
        self.article = get_object_or_404(Article, slug=slug)
        comments = Comment.objects.filter(article=self.article)
        commentCount = comments.count()
        serializer = self.serializer_class(comments, many=True)
        return Response({

            "comments": serializer.data,
            "commentCount": commentCount
        }, status=status.HTTP_200_OK)


class CommentDetailView(GenericAPIView):
    """
    Enables users to view details of a specific comment

    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, *args, **kwargs):
        """
        get details of a specific ariticle
        Args:
            pk: comment primary key unique to a comment
        Returns:
            content: returns contents of the comment or 404 if not found
        """
        pk = kwargs.get("pk")
        self.comment = get_object_or_404(Comment, pk=pk)
        serializer = self.serializer_class(self.comment)
        return Response({
            "comment": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, *args, **kwargs):
        pk = kwargs.get("pk")
        return update_obj(self.request, pk, Comment, self.serializer_class)

    def delete(self, request, slug, pk):
        """
        delete a comment given you wrote the comment
        Args:
            slug: this a slug for a particular article
            pk: comment primary key unique to a comment
        Returns:
            content: returns  a message succesfully deleted 
        """
        self.comment = get_object_or_404(Comment, pk=pk)
        check_if_is_author(self.comment, self.request)
        self.comment.delete()
        return Response({
            'message': 'comment deleted successfully'
        }, status=status.HTTP_200_OK)


class CommentLikeView(GenericAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def put(self, *args, **kwargs):
        """
        like or unlike a specific comment
        Args:
            pk[integer]:primary key for a specific comment
        Returns:
            success message and 200 ok if complete else 404 if
            comment is not found
        """
        self.comment = get_object_or_404(Comment, pk=kwargs.get("pk"))
        self.userProfile = get_object_or_404(Profile, user=self.request.user)
        try:
            CommentLike.objects.get(liked_by=self.userProfile,comment_id=self.comment)
        except CommentLike.DoesNotExist:
            serializer = self.serializer_class(data={})
            serializer.is_valid(raise_exception=True)
            serializer.save(liked_by=self.userProfile,
                            comment=self.comment, like_status=True)
            return Response({
                "message": "comment liked successfully"
            }, status=status.HTTP_200_OK)

        return Response({
            "message": "you already liked this comment"
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, *args, **kwargs):
        """
        get all likes of a comment

        Returns:
            likes count for a comment and list of profiles that liked the comment
        """
        self.comment = get_object_or_404(Comment, pk=kwargs.get("pk"))
        self.likes = CommentLike.objects.filter(
            like_status=True).filter(comment=self.comment)
        serializer = self.serializer_class(self.likes, many=True)
        return Response({
            "likes": serializer.data,
            "likesCount": self.likes.count()
        }, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        """
        delete a comment like provided you already liked it

        Returns:
            200 ok if unliking was successful and 400 if user has not liked comment before
        """
        try:
            self.userProfile = get_object_or_404(
                Profile, user=self.request.user)
            self.comment = get_object_or_404(Comment, pk=kwargs.get("pk"))
            CommentLike.objects.get(liked_by=self.userProfile)
        except CommentLike.DoesNotExist:
            return Response({
                'message': 'you have not yet liked this comment'
            }, status=status.HTTP_400_BAD_REQUEST)
        CommentLike.objects.get(liked_by=self.userProfile).delete()
        return Response({
            "message": "unliked comment successfully"
        }, status=status.HTTP_200_OK)


class CommentHistoryView(generics.ListAPIView):
    serializer_class = CommentHistorySerailizer
    permission_classes = (IsAuthenticated, )
    renderer_classes = (CommentJSONRenderer, )

    def get(self, *args, **kwargs):
        article = get_object_or_404(Article, slug=kwargs.get('slug'))
        comment = get_object_or_404(Comment, id=kwargs.get('pk'))
        check_if_can_track_history(article, comment, self.request)
        serializer = self.serializer_class(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
