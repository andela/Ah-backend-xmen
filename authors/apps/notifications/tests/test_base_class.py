from django.test import TestCase
from authors.apps.authentication.models import User
from rest_framework.test import APIClient
from django.urls import reverse
import json
from authors.apps.notifications.models import Notification


class BaseTestClass(TestCase):
    def setUp(self):
       
        self.verified_user = User.objects.create_user(
            username='testuser1',
            email='testemail1@test.com',
            password='testpassworD12')

        self.verified_user_login_credentials = {
            "user": {
                "email": "testemail@test.com",
                "password": "testpassworD12"
            }
        }
        self.test_user2_login = {
            "user": {
                "email": "testemail2@test.com",
                "password": "testpassworD12"
            }
        }
        self.test_user3_login = {
            "user": {
                "email": "testemail3@test.com",
                "password": "testpassworD12"
            }
        }
        self.client = APIClient()

        self.test_user = User.objects.create_user(
            username='testuser',
            email='testemail@test.com', password='testpassworD12')
        self.test_user2 = User.objects.create_user(
            username='testuser2',
            email='testemail2@test.com', password='testpassworD12')
        self.test_user3 = User.objects.create_user(
            username='testuser3',
            email='testemail3@test.com', password='testpassworD12')

        sign_up_response = self.client.post(reverse('authentication:login'),
                                            content_type='application/json', data=json.dumps(self.verified_user_login_credentials))

        self.test_user_token = sign_up_response.data['token']
        self.article = {
            "title": "hello worlfd",
            "description": "desctriptuo",
            "body": 'boddydydabagd'
        }
        

    def add_demo_notifications(self):
        notice = Notification.objects.create_notification(
            sender=self.test_user2.profile,
            receiver=self.test_user.profile,
            message="Your article has received a new comment"
            )
        notice.is_read = True
        notice.save()
        notice = Notification.objects.create_notification(
            sender=self.test_user2.profile,
            receiver=self.test_user.profile,
            message="Your article has received a new like"
            )
        notice = Notification.objects.create_notification(
            sender=self.test_user2.profile,
            receiver=self.test_user.profile,
            message="Your article has been favourited"
            )
        
