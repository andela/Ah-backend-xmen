from rest_framework import serializers
from .models import Comment,CommentReply
from authors.apps.articles.serializers import AuthorProfileSerializer

class ReplyCommentSerializer(serializers.ModelSerializer):
    author=AuthorProfileSerializer(read_only=True)
    class Meta:
        model=CommentReply
        fields=('id','reply_body','repliedOn','updatedOn','author')




class CommentSerializer(serializers.ModelSerializer):
    author=AuthorProfileSerializer(read_only=True)
    class Meta:
        model=Comment
        fields=('id','createdAt','updatedAt','body','author',)
        read_only_fields=('userProfile',)
