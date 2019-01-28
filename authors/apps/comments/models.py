from django.db import models
from authors.apps.articles.models import Article
from authors.apps.profiles.models import Profile

class Comment(models.Model):
    """
    Handles CRUD on a comment that has been made on article
    """
    body=models.TextField(max_length=500)
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
    author=models.ForeignKey(Profile,on_delete=models.CASCADE)
    article=models.ForeignKey(Article,on_delete=models.CASCADE)

    class Meta:
        ordering=['-createdAt']
    
    def __str__(self):
        return self.body

class CommentReply(models.Model):
    """
    Handles replying on a specific comment by made on an article
    """
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='replies')
    reply_body=models.TextField()
    repliedOn=models.DateTimeField(auto_now_add=True)
    updatedOn=models.DateTimeField(auto_now=True)
    author=models.ForeignKey(Profile,on_delete=models.CASCADE)

    class Meta:
        ordering=['repliedOn']
    
    def __str__(self):
        return self.reply_body


class CommentLike(models.Model):
    """
    Handles liking of a specific user by an authenticated user
    """
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)
    like_status=models.BooleanField()
    liked_by=models.ForeignKey(Profile,on_delete=models.CASCADE)

    def __str__(self):
        return "like by  {}".format(self.liked_by)

class CommentReplyLike(models.Model):
    """
    Holds data for liking reply made a comment
    """
    liked=models.BooleanField()
    reply_like_by=models.ForeignKey(Profile,on_delete=models.CASCADE)
    comment_reply=models.ForeignKey(CommentReply,on_delete=models.CASCADE)

    def __str__(self):
        return "reply liked by {}".format(self.reply_like_by)