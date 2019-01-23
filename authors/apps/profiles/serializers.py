from rest_framework import serializers

from .models import Profile
from authors.apps.authentication.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'username',
            'first_name',
            'last_name',
            'created_at',
            'bio',
            'is_following',
            'date_of_birth',
            'image',
            'followers',
            'following'
        ]

    def get_username(self, obj):
        return f"{obj.user.username}"

    def get_followers(self,obj):
        """ 
        This method returns the number of followers for a given user.

        Args: 
            obj(instance): This is a profile instance of a user

        """
        followers = []
        for user in list(obj.followers.all()):
            followers.append(user.username)
        return len(followers)

    def get_following(self,obj):
        """
        A method to returns the number of authors a user is following

        Args: 
            obj(instance): This is a profile instance of a user

        """
        following = []
        visitor = None
        request = self.context.get("request")
        if not request:
            return 
        if not isinstance(request.user, User):
            return
        visitor = request.user
        for profile in visitor.is_following.all():
            following.append(profile.user.username)
        return len(following)

    def get_is_following(self,obj):
        """
        Sets the following status in a user's profile
        """
        visitor = self.context['request'].user
        return True if visitor in obj.followers.all() else False


class ProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(source="User")
    class Meta:
        extra_kwargs ={
            'username':{
                'read_only':True
            }
        }
        model = Profile
        fields = [
            'username',
            'first_name',
            'last_name',
            'bio',
            'image',
            'date_of_birth',
            'followers'
        ]
     
    def get_username(self, obj):
        return f"{obj.user.username}"

    def to_representation(self, instance):
        """
         Args: 
           instance :(Django model instance)
        
        Returns: 
            Dictionary representation of the custom object
            This is to allow us customize how the serialized data is rendered
        """
        return {
            "profile":{
                "first_name":instance.first_name, 
                "last_name": instance.last_name,
                "bio": instance.bio,
                "image":instance.image or None, # put null if no image was uploaded
                "date_of_birth": instance.date_of_birth
             } 
        }


class ProfileListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = [
            'username',
            'first_name',
            'last_name',
            'bio',
            'image'
        ]
    
    def get_username(self, obj):
        return f"{obj.user.username}"
