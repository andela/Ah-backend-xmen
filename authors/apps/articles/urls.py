from django.urls import path
from . import views


urlpatterns = [
    path('', views.ArticleListCreateView.as_view(), name='article-create'),
    path('favorites', views.FavoritesView.as_view(), name='favorite-articles'),
    path('<slug>/', views.ArticleUpdateDeleteView.as_view(), name='article-update'),
    path('<slug>/likes/', views.ArticleLikesView.as_view(), name='article-likes'),
    path('<slug>/bookmark', views.BookmarkAPIView.as_view(), name='article-bookmark'),
    path('<slug>/rate/', views.RatingsAPIView.as_view(), name='article-rates'),
    path('<slug>/favorite', views.FavoriteHandlerView.as_view(), name='article-favorite'),
]
