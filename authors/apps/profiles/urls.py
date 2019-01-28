from django.urls import path
from .views import (
    UserProfileView,
    UserProfileUpdateView,
    UserProfileListView,
    FollowView, 
    FollowersView,
    FollowingView
)


urlpatterns = [
    path('', UserProfileListView.as_view(), name='profile-list'),
    path('<username>', UserProfileView.as_view(), name='profile-detail'),
    path('<username>/edit', UserProfileUpdateView.as_view(), name='profile-update'),
    path('<username>/follow', FollowView.as_view(), name='follow'),
    path('<username>/following', FollowingView.as_view(), name='following'),
    path('<username>/followers', FollowersView.as_view(), name='followers')

]
