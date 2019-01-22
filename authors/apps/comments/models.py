from django.db import models
from authors.apps.articles.models import Article
from authors.apps.profiles.models import Profile

class Comment(models.Model):
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
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='replies')
    reply_body=models.TextField()
    repliedOn=models.DateTimeField(auto_now_add=True)
    updatedOn=models.DateTimeField(auto_now=True)
    author=models.ForeignKey(Profile,on_delete=models.CASCADE)

    class Meta:
        ordering=['repliedOn']
    
    def __str__(self):
        return self.reply_body


