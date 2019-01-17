from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import (
    IsAuthenticated,
)

from .models import Profile
from .serializers import (
    UserProfileSerializer,
    ProfileUpdateSerializer
)
from authors.apps.utils.messages import error_messages
from .renderers import UserProfileJSONRenderer

from authors.apps.utils.custom_permissions.permissions import if_owner_permission


class UserProfileView(generics.RetrieveAPIView):
    """ Fetches and displays the details
    of a user profile to the currently
    logged in person
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    renderer_classes = (UserProfileJSONRenderer, )

    def get_object(self, *args, **kwargs):
        username = self.kwargs.get("username")
        return get_object_or_404(Profile, user__username=username)


class UserProfileUpdateView(generics.UpdateAPIView):
    """ Allows the currently logged in user
    to edit their user profile
    possible edittable fields include,
    first_name, last_name, bio
    and image """
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        if_owner_permission(self.request, **self.kwargs)
        username = self.kwargs.get("username")
        return get_object_or_404(Profile, user__username=username)
