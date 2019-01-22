from django.urls import path
from .views import CommentView,CommentDetailView,CommentReplyView,CommentReplyDetailView

urlpatterns = [
     path('<slug>/comments/',CommentView.as_view(),name='comments'),
    path('<slug>/comments/<int:pk>/',CommentDetailView.as_view(),name='comment-detail'),
    path('<slug>/comments/<int:pk>/reply/',CommentReplyView.as_view(),name='comment-reply'),
    path('<slug>/comments/<int:pk>/reply/<int:reply_id>/',CommentReplyDetailView.as_view(),name='comment-reply-detail')
]


