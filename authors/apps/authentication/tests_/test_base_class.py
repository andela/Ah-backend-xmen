from django.test import TestCase
from authors.apps.authentication.models import User
from rest_framework.test import APIClient
from django.urls import reverse
import json


class BaseTestClass(TestCase):
    def setUp(self):
        self.user_data = {
            "user": {
                "username": "Jacob",
                "email": "jake@jake.jake",
                "password": "JakeJake12"
            }
        }
        self.user_data_weak_password = {
            "user": {
                "username": "Jacob",
                "email": "jake@jake.jake",
                "password": "jakejake"
            }
        }
        self.user_data_short_password = {
            "user": {
                "username": "Jacob",
                "email": "jake@jake.jake",
                "password": "jake"
            }
        }

        self.user2_data = {
            "user": {
                "username": "Jacob1",
                "email": "jake1@jake.jake",
                "password": "JakeJake12"
            }
        }

        self.update_data = {
            "first_name": "Soultech",
            "last_name": "Muhwezi",
            "bio": "Sample bio data"
        }

        self.same_email_user = {
            "user": {
                "username": "Jackson",
                "email": "jake@jake.jake",
                "password": "jAckson5"
            }
        }

        self.same_username_user = {
            "user": {
                "username": "Jacob",
                "email": "jake@gmail.com",
                "password": "jAcobson10"
            }
        }
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
        self.verified_user_forgot_password = {
            "user": {
                "email": "testemail@test.com"
            }
        }
        self.invalid_user = {
            "user": {
                "email": "adddd@gmail.com",
                "password": "Aaddadasas"

            }
        }

        self.client = APIClient()

        self.test_user = User.objects.create_user(
            username='testuser',
            email='testemail@test.com', password='testpassworD12')

        self.client = APIClient()

        sign_up_response = self.client.post(
            reverse('authentication:login'),
            content_type='application/json',
            data=json.dumps(self.verified_user_login_credentials))

        self.test_user_token = sign_up_response.data['token']
