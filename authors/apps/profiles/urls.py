from django.urls import path
from .views import (
    UserProfileView,
    UserProfileUpdateView,
)


urlpatterns = [
    path('<username>', UserProfileView.as_view(), name='profile-detail'),
    path('<username>/edit', UserProfileUpdateView.as_view(), name='profile-update')
]
