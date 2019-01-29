from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    receiver = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'sender',
            'receiver',
            'message',
            'is_read',
            'action_link',
            'created_at'
        ]

    def get_sender(self, obj):
        return obj.sender.user.username

    def get_receiver(self, obj):
        return obj.receiver.user.username
