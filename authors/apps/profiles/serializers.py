from rest_framework import serializers
from .models import Profile


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'username',
            'first_name',
            'last_name',
            'created_at',
            'bio',
            'following',
            'date_of_birth',
            'image'
        ]

    def get_username(self, obj):
        return f"{obj.user.username}"


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
            'date_of_birth'
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
