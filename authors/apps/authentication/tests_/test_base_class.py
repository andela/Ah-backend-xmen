from django.test import TestCase
from authors.apps.authentication.models import User
from rest_framework.test import APIClient


class BaseTestClass(TestCase):
    def setUp(self):
        self.user_data = {
            "user": {
                "username": "Jacob",
                "email": "jake@jake.jake",
                "password": "JakeJake12"
            }
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
            username='testuser', email='testemail@test.com', password='testpassworD12')

        self.verified_user_login_credentials = {
            "user": {
                "email": "testemail@test.com",
                "password": "testpassworD12"
            }
        }

        self.invalid_user = {
            "user": {
                "email": "adddd@gmail.com",
                "password": "Aaddadasas"

            }
        }

        self.client = APIClient()
