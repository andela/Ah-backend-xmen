from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ReplyLikeSerializer, ReplyCommentSerializer, ReplyHistorySerailizer
from authors.apps.profiles.models import Profile
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User
from .models import CommentReplyLike, Comment, CommentLike, CommentReply
from django.shortcuts import get_object_or_404
from .utils import update_obj
from authors.apps.utils.custom_permissions.permissions import (
    check_if_is_author)
from .renderers import ReplyJSONRenderer
from ..utils.custom_permissions.permissions import check_if_can_track_history


class CommentReplyView(GenericAPIView):

    serializer_class = ReplyCommentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        """
        delete a comment given you wrote the comment
        Args:
            pk: pk for a comment on which a reply is to be posted
        Returns:
            content: returns reply message data
        """
        pk = kwargs.get("pk")
        self.userProfile = get_object_or_404(Profile, user=self.request.user)
        self.comment = get_object_or_404(Comment, pk=pk)
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.userProfile, comment=self.comment)
        return Response(
            {"reply": serializer.data}, status=status.HTTP_201_CREATED
        )

    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        self.comment = get_object_or_404(Comment, pk=pk)
        self.comment_replies = CommentReply.objects.filter(
            comment=self.comment)
        repliesCount = CommentReply.objects.filter(
            comment=self.comment).count()
        serializer = self.serializer_class(self.comment_replies, many=True)
        return Response({
            "replies": serializer.data,
            "repliesCount": repliesCount

        }, status=status.HTTP_200_OK)


class CommentReplyDetailView(GenericAPIView):
    """
    This view enables viewing detials of a specific comment given your 
    are authenticated
    """
    serializer_class = ReplyCommentSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        """
        Get All replies of a comment given 
        Args:
            reply_id:Pk for a given reply
        Returns:
            content: returns details of a specific reply
        """
        reply_id = kwargs.get("reply_id")
        self.replyDetail = get_object_or_404(CommentReply, pk=reply_id)
        self.user = get_object_or_404(User, profile=self.replyDetail.author)
        self.authorProfile = get_object_or_404(Profile, user=self.user)
        reply_data = {
            "id": self.replyDetail.pk,
            "reply_body": self.replyDetail.reply_body,
            "updatedOn": self.replyDetail.updatedOn,
            "repliedOn": self.replyDetail.repliedOn,
            "author": {
                "bio": self.authorProfile.bio,
                "username": self.user.username,
                "image": str(self.authorProfile.image),
                "following": self.authorProfile.following
            }
        }

        return Response({
            "reply": reply_data
        }, status=status.HTTP_200_OK)

    def put(self, *args, **kwargs):
        reply_id = kwargs.get("reply_id")
        return update_obj(self.request, reply_id, CommentReply, self.serializer_class)

    def delete(self, *args, **kwargs):
        """
        Delete a given reply given you are the author of the reply
        Args:
            reply_id:id for a reply object
        Returns:
            content: returns a message reply deleted successfully if okay
            raises:permission if person performing action is not author of comment
        """
        reply_id = kwargs.get("reply_id")
        self.replyDetail = get_object_or_404(CommentReply, pk=reply_id)
        check_if_is_author(self.replyDetail, self.request)
        self.replyDetail.delete()
        return Response({
            "message": "reply delete successfully"
        }, status=status.HTTP_200_OK)


class CommentReplyLikeView(GenericAPIView):
    serializer_class = ReplyLikeSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, *args, **kwargs):
        """
        like a specific reply on a comment
        Args:
            reply_id[integer]:primary key for a comment
            pk[integer]:identifier for a comment
        Returns:
            200 ok if like was successful else 400 if user tries to like same reply
        """
        try:
            self.comment = get_object_or_404(Comment, pk=kwargs.get("pk"))
            self.userProfile = get_object_or_404(
                Profile, user=self.request.user)
            self.commentReply = get_object_or_404(
                CommentReply, pk=kwargs.get("reply_id"))
            CommentReplyLike.objects.get(reply_like_by=self.userProfile)
           
        except CommentReplyLike.DoesNotExist:
            serializer = self.serializer_class(data={})
            serializer.is_valid(raise_exception=True)
            serializer.save(
                liked=True, comment_reply=self.commentReply, reply_like_by=self.userProfile)
            return Response({
                "message": "reply been liked successfully"
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "you already liked this reply"
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, *args, **kwargs):
        """
        Get all Reply likes on a specific comment reply
        Args:
            reply_id[integer]:primary key of the reply
        Returns:
            reply likes count and user profiles who liked the reply
        """
        self.commentReply = get_object_or_404(
            CommentReply, pk=kwargs.get("reply_id"))
        self.reply_likes = CommentReplyLike.objects.filter(
            liked=True).filter(comment_reply=self.commentReply)
        serializer = self.serializer_class(self.reply_likes, many=True)
        return Response({
            "reply_likes": serializer.data,
            "replyLikesCount": self.reply_likes.count()
        })

    def delete(self, *args, **kwargs):
        """
        Unlike a comment reply
        Args:
            reply[id]:primary key a comment reply
        Returns:
            200 ok if comment reply is unliked
            400 bad request if user has not liked comment reply before
        """
        self.userProfile = get_object_or_404(Profile, user=self.request.user)
        self.commentReply = get_object_or_404(
            CommentReply, pk=kwargs.get("reply_id"))
        try:
            CommentReplyLike.objects.get(reply_like_by=self.userProfile)
        except CommentReplyLike.DoesNotExist:
            return Response({
                "message": "you havent liked this reply yet"
            }, status=status.HTTP_400_BAD_REQUEST)
        CommentReplyLike.objects.get(reply_like_by=self.userProfile).delete()
        return Response({
            "message": "unliked reply successfully"
        }, status=status.HTTP_200_OK)


class ReplyHistoryView(ListAPIView):
    serializer_class = ReplyHistorySerailizer
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ReplyJSONRenderer, )

    def get(self, *args, **kwargs):
        article = get_object_or_404(Article, slug=kwargs.get('slug'))
        get_object_or_404(Comment, id=kwargs.get('pk'))
        reply = get_object_or_404(CommentReply, id=kwargs.get('pk'))
        check_if_can_track_history(article, reply, self.request)
        serializer = self.serializer_class(reply)
        return Response(serializer.data, status=status.HTTP_200_OK)
