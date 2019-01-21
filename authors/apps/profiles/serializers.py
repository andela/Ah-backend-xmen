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
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'bio',
            'image',
            'date_of_birth'
        ]
