from django.test import TestCase
from authors.apps.notifications.models import Notification, NotificationManager
from authors.apps.profiles.models import Profile
from authors.apps.authentication.models import User


class TestModel(TestCase):
    def _create_notification(self, sender=None, receiver=None, message=None):
        with self.assertRaises(TypeError):
            Notification.objects.create_notification(
                sender=sender,
                receiver=receiver,
                message=message
                )

    def _create_profile(self):
        user = User.objects.create(username='jake2', email='jake2@jake.jake')
        return Profile.objects.get(user=user)
 
    def test_create_notification_missing_sender_and_receiver_fails(self):
        with self.assertRaises(TypeError):
            Notification.objects.create_notification(
                sender=None,
                receiver=None,
                message="Your article has received a new comment"
                )

    def test_create_notification_missing_sender_fails(self):
        receiver = self._create_profile()
        self._create_notification(
            None, receiver, "Your article has received a new comment")

    def test_create_notification_missing_receiver_fails(self):
        sender = self._create_profile()
        self._create_notification(
            sender, None, "Your article has received a new comment")
       
    def test_create_notification_missing_message_fails(self):
        r_user = User.objects.create(username='jake', email='jake@jake.jake')
        receiver = Profile.objects.get(user=r_user)
        s_user = User.objects.create(username='jake2', email='jake2@jake.jake')
        sender = Profile.objects.get(user=s_user)
        with self.assertRaises(TypeError):
            Notification.objects.create_notification(
                 sender=sender,
                 receiver=receiver,
                 message=None
                )

    def test_create_notification_valid_data_succeeds(self):
        r_user = User.objects.create(username='jake', email='jake@jake.jake')
        receiver = Profile.objects.get(user=r_user)
        s_user = User.objects.create(username='jake1', email='jake1@jake.jake')
        sender = Profile.objects.get(user=s_user)
        notice = Notification.objects.create_notification(
            sender=sender,
            receiver=receiver,
            message="Your article has received a new comment"
            )
        self.assertIn(notice, Notification.objects.all())

    def test_get_all_notifications_succeeds(self):
        r_user = User.objects.create(username='jake', email='jake@jake.jake')
        receiver = Profile.objects.get(user=r_user)
        s_user = User.objects.create(username='jake1', email='jake1@jake.jake')
        sender = Profile.objects.get(user=s_user)
        Notification.objects.create_notification(
            sender=sender,
            receiver=receiver,
            message="Your article has received a new comment"
            )
        notices = Notification.objects.get_all(receiver)
        self.assertEqual(1,len(list(notices)))

    def test_get_unread_notifications_succeeds(self):
        r_user = User.objects.create(username='jake', email='jake@jake.jake')
        receiver = Profile.objects.get(user=r_user)
        s_user = User.objects.create(username='jake1', email='jake1@jake.jake')
        sender = Profile.objects.get(user=s_user)
        notice = Notification.objects.create_notification(
            sender=sender,
            receiver=receiver,
            message="Your article has received a new comment"
            )
        notice.is_read = True
        notice.save()
        Notification.objects.create_notification(
            sender=sender,
            receiver=receiver,
            message="Your article has received a new comment"
            )
        all_notices = Notification.objects.get_all(receiver)
        self.assertEqual(2, len(list(all_notices)))

        unread_notices = Notification.objects.get_unread(receiver)
        self.assertEqual(1, len(list(unread_notices)))

        Notification.objects.mark_all_as_read(receiver)
        unread_notices = Notification.objects.get_unread(receiver)
        self.assertEqual(0, len(list(unread_notices)))

