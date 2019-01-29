from django.urls import path
from authors.apps.articles.views import views
from authors.apps.articles.views import bookmark_views


urlpatterns = [
    path('', views.ArticleListCreateView.as_view(), name='article-create'),
    path('favorites', views.FavoritesView.as_view(), name='favorite-articles'),
    path('<slug>/', views.ArticleUpdateDeleteView.as_view(), name='article-update'),
    path('<slug>/likes/', views.ArticleLikesView.as_view(), name='article-likes'),
    path('<slug>/bookmark', bookmark_views.BookmarkAPIView.as_view(), name='article-bookmark'),
    path('<slug>/rate/', views.RatingsAPIView.as_view(), name='article-rates'),
    path('<slug>/favorite', views.FavoriteHandlerView.as_view(), name='article-favorite'),
    path('<slug>/report', views.ReportArticleView.as_view(), name='flag'),
    
]
