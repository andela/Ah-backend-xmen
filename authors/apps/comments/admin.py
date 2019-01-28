from django.contrib import admin
from .models import Comment,CommentLike,CommentReply

admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(CommentReply)
