from authors.apps.profiles.models import Profile
from django.db import models
from authors.apps.utils.messages import notification_mesages


class NotificationManager(models.Manager):
    
    def create_notification(self, sender, receiver, message, action_link=None):
        """Create and return a  notification"""
        
        if sender not in Profile.objects.all():
            raise TypeError(
                notification_mesages['missing_field'].format('sender'))

        if receiver not in Profile.objects.all():
            missing_field = 'receiver'
            raise TypeError(
                notification_mesages['missing_field'].format(missing_field))
        if message is None:
            raise TypeError('message must be a String')
        notification = self.model(
            sender=sender, receiver=receiver,
            message=message, action_link=action_link)
        notification.save()
        return notification

    def get_unread(self, receiver):
        return self.filter(receiver=receiver, is_read=False)

    def get_all(self, receiver):
        return self.filter(receiver=receiver)

    def mark_all_as_read(self, receiver):
        notifications = self.get_unread(receiver)
        for notification in notifications:
            notification.is_read = True
            notification.save()


class Notification(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE,
        related_name='received_notifications')

    is_read = models.BooleanField(default=False)
    message = models.CharField(max_length=255)
    action_link = models.CharField(max_length=255, blank=True, null=True)
    is_emailed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = NotificationManager()

    def __str__(self):

        """
        Returns a string representation of this `Notification`.

        This string is used when a `Notification` is printed in the console.
        """

        return self.message
