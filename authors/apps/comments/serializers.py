from rest_framework import serializers
from .models import Comment, CommentReply, CommentLike, CommentReplyLike
from authors.apps.articles.serializers import AuthorProfileSerializer


class ReplyCommentSerializer(serializers.ModelSerializer):
    author = AuthorProfileSerializer(read_only=True)

    class Meta:
        model = CommentReply
        fields = ('id', 'reply_body', 'repliedOn', 'updatedOn', 'author')


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'createdAt', 'updatedAt', 'body', 'author',)
        read_only_fields = ('userProfile',)


class CommentLikeSerializer(serializers.ModelSerializer):
    liked_by = AuthorProfileSerializer(read_only=True)
    """
    A comment like serializer
    """
    class Meta:
        model = CommentLike
        fields = ('liked_by',)
        read_only_fields = ('like_status', 'liked_by')


class ReplyLikeSerializer(serializers.ModelSerializer):
    reply_like_by = AuthorProfileSerializer(required=False)

    class Meta:
        fields = ('reply_like_by',)
        read_only_fields = ('reply_like_by',)
        model = CommentReplyLike
