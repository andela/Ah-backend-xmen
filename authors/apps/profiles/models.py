from datetime import date
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from authors.apps.utils.messages import error_messages
from rest_framework.serializers import ValidationError

from authors.apps.authentication.models import User


UserModel = getattr(settings, "AUTH_USER_MODEL", User)


class ProfileManager(models.Manager):
    """
    Contains the methods to follow and unfollow a user profile 
    """
    def follow_author(self, request_user, new_author):
        user_to_follow = get_object_or_404(User, username=new_author)
        follow = get_object_or_404(Profile, user=user_to_follow)
        user = request_user
        if follow == user.profile:
            raise ValidationError(error_messages['follow denied'])
        if user in follow.followers.all():
            raise ValidationError(error_messages['already follow'].format(follow.user.username))
        else:
            follow.followers.add(user)
            is_following = True
        return follow,is_following

    def unfollow_author(self, request_user, author):
        user_to_unfollow = get_object_or_404(User, username=author)
        follow = get_object_or_404(Profile, user=user_to_unfollow)
        user = request_user
        if follow == user.profile:
            raise ValidationError(error_messages['unfollow denied'])
        if user in follow.followers.all():
            follow.followers.remove(user)
            is_following = False
        else:
            raise ValidationError(error_messages['not follow'].format(follow.user.username))
        return follow, is_following


class Profile(models.Model):
    """
       Create a data model to hold more information,
       about our awesome users.
       It is through profiles that we get to know
       more about the name behind a user account.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    date_of_birth = models.DateField(_("Date"), blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='is_following', blank=True) 
    # to access the profiles an author is following, make use of user1.is_following.all() 
    #to access followers of a profile, make use of profile1.followers.al()
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='profile/images/',
        blank=True)
    following = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}"


def user_post_save_receiver(instance, created, *args, **kwargs):
    """
    Handle creating the profile when a user finishes
    the signup process
    """
    if created:
        Profile.objects.get_or_create(
            user=instance
        )
post_save.connect(user_post_save_receiver, sender=User)
