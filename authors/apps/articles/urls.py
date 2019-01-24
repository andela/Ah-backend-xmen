from django.urls import path
from . import views


urlpatterns = [
    path('', views.ArticleListCreateView.as_view(), name='article-create'),
    path('<slug>/', views.ArticleUpdateDeleteView.as_view(), name='article-update'),
   
]
