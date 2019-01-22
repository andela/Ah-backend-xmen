from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CommentSerializer
from authors.apps.profiles.models import Profile
from authors.apps.articles.models import Article
from .models import Comment
from django.shortcuts import get_object_or_404
from authors.apps.utils.custom_permissions.permissions import check_if_is_commentor

class CommentView(GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=CommentSerializer
    def post(self,request,slug):
        self.author=get_object_or_404(Profile,user=request.user)
        self.article=get_object_or_404(Article,slug=slug)
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.author,article=self.article)
        return Response({
            'comment':serializer.data
        },status=status.HTTP_201_CREATED)
    
    def get(self,request,slug):
        self.article=get_object_or_404(Article,slug=slug)
        comments=Comment.objects.filter(article=self.article)
        commentCount=comments.count()
        serializer=self.serializer_class(comments,many=True)
        return Response({
            
            "comments":serializer.data,
            "commentCount":commentCount
        },status=status.HTTP_200_OK)


class CommentDetailView(GenericAPIView):
    serializer_class=CommentSerializer
    permission_classes=(IsAuthenticated,)

    def get(self,request,slug,pk):
        self.comment=get_object_or_404(Comment,pk=pk)
        serializer=self.serializer_class(self.comment)
        return Response({
            "comment":serializer.data
        },status=status.HTTP_200_OK)
    
    def put(self,request,slug,pk):
        self.comment=get_object_or_404(Comment,pk=pk)
        check_if_is_commentor(self.comment,self.request)
        serializer=self.serializer_class(self.comment,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "comment":serializer.data,
        },status=status.HTTP_201_CREATED)
    
    def delete(self,request,slug,pk):
        self.comment=get_object_or_404(Comment,pk=pk)
        check_if_is_commentor(self.comment,self.request)
        self.comment.delete()
        return Response({
            'message':'comment deleted successfully'
        },status=status.HTTP_200_OK)

        
        

