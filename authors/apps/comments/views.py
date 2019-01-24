from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CommentSerializer,ReplyCommentSerializer
from authors.apps.profiles.models import Profile
from authors.apps.articles.models import Article
from .models import Comment,CommentReply
from django.shortcuts import get_object_or_404
from authors.apps.utils.custom_permissions.permissions import check_if_is_author
from authors.apps.authentication.models import User


def update_obj(request,id,Instance,serializer_class):
    """
    this function handles updating of a model 
    Args:
        request: a request object
        id:id of the object to be updated
        Instance:Class instance of the model to which the object belongs to
        serializer_class:serializer class of the current view
    Returns:
        201 code if successful else False if updating fails
    """
    obj=get_object_or_404(Instance,pk=id)
    check_if_is_author(obj,request)
    serializer=serializer_class(obj,data=request.data,partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({
        'data':serializer.data
    },status=status.HTTP_201_CREATED)

class CommentView(GenericAPIView):
    """
    Allows authenticated users to post a comment on an articles 
    and also view all comments on an article
    """
    permission_classes=(IsAuthenticated,)
    serializer_class=CommentSerializer

    def post(self,request,slug):
        """
        Allows authenticated users can add comments on articles

        Args:
            slug: this a slug for a particular article
        Returns:
            code: The return 201 created for success
        
        """
        self.author=get_object_or_404(Profile,user=request.user)
        self.article=get_object_or_404(Article,slug=slug)
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.author,article=self.article)
        return Response({
            'comment':serializer.data
        },status=status.HTTP_201_CREATED)
    
    def get(self,request,slug):
        """
        get all comments on an article

        Args:
            param1 (slug): this a slug for a particular article
        Returns:
            code: The return 201 created for success
        """
        self.article=get_object_or_404(Article,slug=slug)
        comments=Comment.objects.filter(article=self.article)
        commentCount=comments.count()
        serializer=self.serializer_class(comments,many=True)
        return Response({
            
            "comments":serializer.data,
            "commentCount":commentCount
        },status=status.HTTP_200_OK)

class CommentDetailView(GenericAPIView):
    """
    Enables users to view details of a specific comment
    
    """
    serializer_class=CommentSerializer
    permission_classes=(IsAuthenticated,)

    def get(self,*args, **kwargs):
        """
        get details of a specific ariticle
        Args:
            pk: comment primary key unique to a comment
        Returns:
            content: returns contents of the comment or 404 if not found
        """
        pk=kwargs.get("pk")
        self.comment=get_object_or_404(Comment,pk=pk)
        serializer=self.serializer_class(self.comment)
        return Response({
            "comment":serializer.data
        },status=status.HTTP_200_OK)
    
    def put(self,*args, **kwargs):
        pk=kwargs.get("pk")
        return update_obj(self.request,pk,Comment,self.serializer_class)
       
    
    def delete(self,request,slug,pk):
        """
        delete a comment given you wrote the comment
        Args:
            slug: this a slug for a particular article
            pk: comment primary key unique to a comment
        Returns:
            content: returns  a message succesfully deleted 
        """
        self.comment=get_object_or_404(Comment,pk=pk)
        check_if_is_author(self.comment,self.request)
        self.comment.delete()
        return Response({
            'message':'comment deleted successfully'
        },status=status.HTTP_200_OK)

        
        
class CommentReplyView(GenericAPIView):

    serializer_class=ReplyCommentSerializer
    permission_classes=(IsAuthenticated,)

    def post(self,*args, **kwargs):
        """
        delete a comment given you wrote the comment
        Args:
            pk: pk for a comment on which a reply is to be posted
        Returns:
            content: returns reply message data
        """
        pk=kwargs.get("pk")
        self.userProfile=get_object_or_404(Profile,user=self.request.user)
        self.comment=get_object_or_404(Comment,pk=pk)
        serializer=self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.userProfile,comment=self.comment)
        return Response(
            {"reply":serializer.data},status=status.HTTP_201_CREATED
        )
    
    def get(self,*args, **kwargs):
        pk=kwargs.get("pk")
        self.comment=get_object_or_404(Comment,pk=pk)
        self.comment_replies=CommentReply.objects.filter(comment=self.comment)
        repliesCount=CommentReply.objects.filter(comment=self.comment).count()
        serializer=self.serializer_class(self.comment_replies,many=True)
        return Response({
            "replies":serializer.data,
            "repliesCount":repliesCount

        },status=status.HTTP_200_OK)


class CommentReplyDetailView(GenericAPIView):
    """
    This view enables viewing detials of a specific comment given your 
    are authenticated
    """
    serializer_class=ReplyCommentSerializer
    permission_classes=(IsAuthenticated,)

    def get(self,*args, **kwargs):
        """
        Get All replies of a comment given 
        Args:
            reply_id:Pk for a given reply
        Returns:
            content: returns details of a specific reply
        """
        reply_id=kwargs.get("reply_id")
        self.replyDetail=get_object_or_404(CommentReply,pk=reply_id)
        self.user=get_object_or_404(User,profile=self.replyDetail.author)
        self.authorProfile=get_object_or_404(Profile,user=self.user)
        reply_data={
            "id":self.replyDetail.pk,
            "reply_body":self.replyDetail.reply_body,
            "updatedOn":self.replyDetail.updatedOn,
            "repliedOn":self.replyDetail.repliedOn,
            "author":{
                "bio":self.authorProfile.bio,
                "username":self.user.username,
                "image":str(self.authorProfile.image),
                "following":self.authorProfile.following
            }
        }

        return Response({
            "reply":reply_data
        },status=status.HTTP_200_OK)

    def put(self,*args, **kwargs):
        reply_id=kwargs.get("reply_id")
        return update_obj(self.request,reply_id,CommentReply,self.serializer_class)


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
        self.replyDetail=get_object_or_404(CommentReply,pk=reply_id)
        check_if_is_author(self.replyDetail,self.request)
        self.replyDetail.delete()
        return Response({
            "message":"reply delete successfully"
        }, status=status.HTTP_200_OK)







