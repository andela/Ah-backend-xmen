from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
import json
from authors.apps.authentication.models import User
from .test_base_class import BaseTestClass


class TestUserEndPoints(BaseTestClass):
    def test_user_regsitration_with_valid_data_succeeds(self):
        resp = self.client.post(reverse('authentication:signup'),
                                content_type='application/json', data=json.dumps(self.user_data))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_login_user_with_valid_data_succeeds(self):
        resp = self.client.post(reverse('authentication:login'), content_type='application/json',
                                data=json.dumps(self.verified_user_login_credentials))
        self.assertEqual(resp.status_code, 200)

    def test_login_with_invalid_user_fails(self):
        expected_response = {
            "errors": {
                "error": [
                    "A user with this email and password was not found."
                ]
            }
        }
        resp = self.client.post(reverse('authentication:login'),
                                content_type='application/json', data=json.dumps(self.invalid_user))
        self.assertDictEqual(resp.data, expected_response)
        self.assertIn(
            "A user with this email and password was not found.", str(resp.data))
