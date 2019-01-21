from django.urls import path
from .views import (
    UserProfileView,
    UserProfileUpdateView,
    UserProfileListView,
)


urlpatterns = [
    path('', UserProfileListView.as_view(), name='profile-list'),
    path('<username>', UserProfileView.as_view(), name='profile-detail'),
    path('<username>/edit', UserProfileUpdateView.as_view(), name='profile-update')
]
