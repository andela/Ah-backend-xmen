from django.urls import path
from . import views

urlpatterns = [
    path('articles/<slug>/comments/',views.CommentView.as_view(),name='comments'),
    path('articles/<slug>/comments/<int:pk>/',views.CommentDetailView.as_view(),name='comment-detail')

]
