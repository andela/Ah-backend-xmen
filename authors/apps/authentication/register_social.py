from .models import User 
from rest_framework import serializers
import uuid


def create_social_user(profile):
    """ 
    This method function is to create a new social
    auth user who might not exist in the database
    """

    if not profile:
        raise serializers.ValidationError('The auth_token is expired or invalid')

    if not isinstance(profile, dict):
        profile = {
            'name': profile.name,
            'email': profile.email
        }

    try:
        social_user = User.objects.get(email=profile.get('email'))
    except User.DoesNotExist as e:
        user = {
            'username': (profile.get('name').replace(" ", "") +str(uuid.uuid1().int)[:3]),
            'email': profile.get('email'),
            'password': User.objects.make_random_password()
        }
        new_social_user = User.objects.create(**user)
        return new_social_user
    return social_user
