from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.core import mail
import json
import re
from .test_data import responses
from .test_base_class import BaseTestClass
from authors.apps.authentication.register_social import create_social_user

from unittest.mock import patch


class TestSocialAuth(BaseTestClass):

    # facebook social login tests
    def tests_facebook_login_fails_invalid_token(self):
        """ 
        Testing function for facebook login that is to fail and it
        takes in a dummy  token that is used to test if it is invalid

        AssertEquals:
            - status code 400 Bad request
        """
        response = self.client.post(reverse('authentication:facebook'), 
                                            content_type = 'application/json', 
                                            data=json.dumps(self.invalid_facebook_token))
        self.assertEqual(response.status_code, 400)


    @patch('authors.apps.authentication.serializers.FacebookSocialAuthSerializer')
    def tests_facebook_login_succeeds(self, mock_facebook_auth):
        """ 
        Function for testing facebook login that is successful and it
        takes in an actual token that is used for testing if it is valid

        AssertEquals:
            - status code 200 Success
        """
        mock_facebook_auth.facebook_verification.return_value = {
            'email': 'testuser@testplatform.testextention',
            'name': 'testuser',
            'id': '12345'
        }
        response = self.client.post(reverse('authentication:facebook'), 
                                            content_type = 'application/json', 
                                            data=json.dumps(self.valid_facebook_token))
        self.assertEqual(response.status_code, 200)


    # Google auth social login tests
    def tests_google_login_fails_invalid_token(self):
        """ 
        This one tests the Google login as it checks if it is valid while
        taking in a dummy token that is used for testing if it is valid

        AssertEquals:
            - status code 400 Bad request
        """
        response = self.client.post(reverse('authentication:google'), 
                                            content_type = 'application/json', 
                                            data=json.dumps(self.invalid_google_token))
        self.assertEqual(response.status_code, 400)


    @patch('authors.apps.authentication.serializers.GoogleSocialAuthSerializer')
    def tests_google_login_succeeds(self, mock_google_auth):
        """ 
        Google login that is successful and it
        takes in an actual token

        AssertEquals:
            - status code 200 Success
        """
        mock_google_auth.google_verification.return_value = {
            'email': 'testuser@testplatform.testextention',
            'name': 'testuser',
            'id': '12345'
        }
        response = self.client.post(reverse('authentication:google'), 
                                            content_type = 'application/json', 
                                            data=json.dumps(self.valid_google_token))
        self.assertEqual(response.status_code, 200)


    # Twitter auth social login tests
    def tests_twitter_login_fails_invalid_token(self):
        response = self.client.post(reverse('authentication:twitter'), 
                                            content_type = 'application/json', 
                                            data=json.dumps(self.invalid_twitter_tokens))
        self.assertEqual(response.status_code, 400)

    @patch('authors.apps.authentication.serializers.TwitterSocialAuthSerializer')
    def tests_twitter_login_succeeds(self, mock_twitter_auth):
        mock_twitter_auth.twitter_verification.return_value = {
            'email': 'testuser11@testplatform.testextention',
            'name': 'testuser11',
            'id': '12345'
        }
        response = self.client.post(reverse('authentication:twitter'), 
                                            content_type = 'application/json', 
                                            data=json.dumps(self.valid_twitter_tokens))
       
        self.assertEqual(response.status_code, 200)
        