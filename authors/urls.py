"""authors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from authors.apps.articles.views import BookmarksListView

schema_view = get_schema_view(
    openapi.Info(
        title="Authors Haven",
        default_version='v1',
        description="A social platform for the creative at heart.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    permission_classes=(AllowAny,),
)
urlpatterns = [

    path('admin/', admin.site.urls),

    path('api/', include(('authors.apps.authentication.urls',
                          'authentication'), namespace='authentication')),
    path('api/documentation/', schema_view.with_ui('swagger',
                                                   cache_timeout=0), name='api_documentation'),
    path('api/articles/', include(('authors.apps.articles.urls','articles'), namespace='articles')),
    path('api/profiles/', include(('authors.apps.profiles.urls','profiles'),  namespace='profiles')),
    path('api/articles/', include(('authors.apps.comments.urls','comments'), namespace='comments')),
    path('api/bookmarks', BookmarksListView.as_view(), name='bookmarks'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
