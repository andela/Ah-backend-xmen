from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.core import mail
import json
import re
from .test_data import responses
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
        expected_response = responses['test_login_with_invalid_user_fails']
        resp = self.client.post(reverse('authentication:login'),
                                content_type='application/json', data=json.dumps(self.invalid_user))
        self.assertDictEqual(resp.data, expected_response)
        self.assertIn( "A user with this email and password was not found.", str(resp.data))

    def test_login_with_missing_email_fails(self):
        expected_response = responses['test_login_with_missing_email_fails']
        self.invalid_user['email']=None
        resp = self.client.post(reverse('authentication:login'),
                                content_type='application/json', data=json.dumps(self.invalid_user))
        self.assertDictEqual(resp.data, expected_response)
       


    def test_user_request_password_reset_link_succeeds(self):
        resp = self.client.post(reverse('authentication:request-password-reset'),
                                 content_type='application/json',
                                 data = json.dumps(self.verified_user_forgot_password)
        )
        self.assertEqual(resp.status_code, 200)
        self.reset_token = resp.data.get('reset-token')
    def test_user_request_password_reset_link_fails(self):
        expected_response = {
            "errors": [
                "User with that email does not exist."
            ]
                }
        resp = self.client.post(reverse('authentication:request-password-reset'),
                                 content_type='application/json',
                                 data = json.dumps(self.invalid_user)
        )
        self.assertDictEqual(resp.data, expected_response)

    def test_user_reset_password_valid_token(self):
        resp = self.client.post(reverse('authentication:request-password-reset'),
                                 content_type='application/json',
                                 data = json.dumps(self.verified_user_forgot_password)
        )
        self.reset_password_url = parse_reset_password_url_from_body(mail.outbox[0].body)
        self.post_data = {
	                "user":{
	                	"password":"New.pass.1"
            	}
            }

        resp = self.client.put(self.reset_password_url,content_type='application/json',
                                  data = json.dumps(self.post_data)
        )
        self.assertEqual(resp.status_code, 200)

    def test_user_reset_password_has_valid_token_succeeds(self):
        resp = self.client.post(reverse('authentication:request-password-reset'),
                                 content_type='application/json',
                                 data = json.dumps(self.verified_user_forgot_password)
        )
        self.reset_password_url = parse_reset_password_url_from_body(mail.outbox[0].body)
        self.post_data = {
	                "user":{
	                	"password":"New.pass.1"
            	}
            }
       
        resp = self.client.get(self.reset_password_url,content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_user_reset_password_has_valid_token_fails(self):
        resp = self.client.post(reverse('authentication:request-password-reset'),
                                 content_type='application/json',
                                 data = json.dumps(self.verified_user_forgot_password)
        )
        self.reset_password_url_invalid = reverse('authentication:password-reset',kwargs={'token':'invalid.jwt.token'})
       
        resp = self.client.get(self.reset_password_url_invalid,content_type='application/json')
        self.assertEqual(resp.status_code, 400)


def parse_reset_password_url_from_body(body):
    urls = re.findall("(?P<url>https?://[^\s]+)", body)
    for url in urls:
        if 'password-reset' in url:
            return url[17:]+'/'

