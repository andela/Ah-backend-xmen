from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status, exceptions
from django.urls import reverse
import json
import jwt
from authors.apps.authentication.models import User
from .test_base_class import BaseTestClass
from datetime import datetime as test_time, timedelta
from django.conf import settings

from unittest.mock import patch, MagicMock

from jwt import ExpiredSignatureError

from authors.apps.authentication.backends import JWTAuthentication


class TestJWTAuthentication(BaseTestClass):
    """Test cases for JWT Authentication"""

    def test_invalid_authorization_header_fails(self):
        """This tests an api endpoint accessed with a wrong authorization header"""
        response = self.client.get(
            '/api/user/', content_type='application/json', HTTP_AUTHORIZATION='invalid token token')

        self.assertIn("Invalid Token", response.data["detail"])

    def test_not_bearer_token(self):
        """This tests an api endpoint accessed using a non Bearer Token in the authorization header"""
        response = self.client.get('/api/user/', content_type='application/json',
                                   HTTP_AUTHORIZATION='Token ' + self.test_user_token)

        self.assertIn("Use a Bearer Token", response.data["detail"])

    def test_invalid_token(self):
        """This tests an api endpoint accessed using an invalid Bearer Token in the authorization header"""
        response = self.client.get('/api/user/', content_type='application/json',
                                   HTTP_AUTHORIZATION='Bearer nhbvjhsjkhfkjsfn,sjk')

        self.assertIn('Invalid token. Could not decode token',
                      response.data["detail"])
