from django.urls import path
from .views import (
     CommentView, CommentDetailView, CommentLikeView, CommentHistoryView)
from .commentReplyViews import (
     CommentReplyView, CommentReplyDetailView,
     CommentReplyLikeView, ReplyHistoryView)

urlpatterns = [
    path('<slug>/comments/', CommentView.as_view(), name='comments'),
    path('<slug>/comments/<int:pk>/',
         CommentDetailView.as_view(), name='comment-detail'),
    path('<slug>/comments/<int:pk>/reply/',
         CommentReplyView.as_view(), name='comment-reply'),
    path('<slug>/comments/<int:pk>/reply/<int:reply_id>/',
         CommentReplyDetailView.as_view(), name='comment-reply-detail'),
    path('<slug>/comments/<int:pk>/reply/<int:reply_id>/like/',
         CommentReplyLikeView.as_view(), name='comment-reply-like'),
    path('<slug>/comments/<int:pk>/like/',
         CommentLikeView.as_view(), name='comment-like'),
    path('<slug>/comments/<int:pk>/history/',
         CommentHistoryView.as_view(), name='comment-history'),
    path('<slug>/comments/<int:pk>/reply/<int:reply_id>/history/',
         ReplyHistoryView.as_view(), name='reply-history')
]
