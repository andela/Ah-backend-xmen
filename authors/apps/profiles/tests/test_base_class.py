from django.test import TestCase
from authors.apps.authentication.models import User
from rest_framework.test import APIClient
from django.urls import reverse
import json


class BaseTestClass(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@gmail.com', password='N0vember')
        
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@gmail.com', password='S3ptemeber')

        self.login_user1 = {
            'user':{
                "email":"user1@gmail.com",
                "password":"N0vember"
            }
        }
        signup_response = self.client.post(reverse('authentication:login'),
                                            content_type='application/json', data=json.dumps(self.login_user1))

        self.user_token = signup_response.data['token']
        self.client = APIClient()

