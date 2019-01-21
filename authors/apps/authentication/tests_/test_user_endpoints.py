from rest_framework import status
from django.urls import reverse
from django.core import mail
import json
import re
from authors.apps.authentication.models import User
from .test_base_class import BaseTestClass


class TestUserEndPoints(BaseTestClass):
    def test_user_regsitration_with_valid_data_succeeds(self):
        resp = self.client.post(reverse('authentication:signup'),
                                content_type='application/json', data=json.dumps(self.user_data))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.user_data['user']['username'], str(resp.data))

    def test_user_email_verification_email_sent(self):
        """ Test email verification email sent """
        self.client.post(reverse('authentication:signup'),
                                  content_type='application/json', data=json.dumps(self.user_data))
        self.assertIn('Email Verification', mail.outbox[0].subject)

    def test_email_verification_succeeds(self):
        resp = self.client.post(reverse('authentication:signup'),
                                content_type='application/json', data=json.dumps(self.user_data))
        """
        Returns:
        on successful signup an a user clicks on the verification link sent to email , a success message
        telling user email has been confirmed is returned
        """

        message = mail.outbox[0].body.split("\n")
        email_activation_url = message.pop(9)
        resp_verification = self.client.get(
            email_activation_url.split("testserver").pop(1))
        self.assertEqual(200, resp_verification.status_code)

    def test_email_verification_fails(self):
        resp = self.client.post(reverse('authentication:signup'),
                                content_type='application/json', data=json.dumps(self.user_data))
        message = mail.outbox[0].body.split("\n")
        email_activation_url = message.pop(9).split("testserver").pop(1)
        User.objects.get(
            username=self.user_data['user']['username']).delete()
        """
            Remove user from database to raise User.DoesntExist exception
            Returns:
            When user is not found and try to activate the deleted users email, its raises a user.DoesNotExist
            Exception with status code 400
        """
        resp_verification = self.client.get(
            email_activation_url)
        self.assertEqual(400, resp_verification.status_code)

    def test_email_verification_fails_invalid_url_token(self):
        resp = self.client.post(reverse('authentication:signup'),
                                content_type='application/json', data=json.dumps(self.user_data))
        message = mail.outbox[0].body.split("\n")
        email_activation_url = message.pop(9).split("testserver").pop(1)
        """
        Args:
        uuid:encoded in url_base_64 with user id
        token:encoded in a hash containing user id

        Returns:
        An error messeage incase the token is has extra characters which may araise if a user makes a typo
        in the link by adding some characters


        """

        self.uuid = email_activation_url.split('/').pop(4)
        self.token = email_activation_url.split('/').pop(5)

        resp_verification = self.client.get(reverse(
            'authentication:email-verification', args=[self.uuid, self.token+"sdd"]))
        self.assertEqual(resp_verification.status_code, 400)

    def test_login_user_with_valid_data(self):
        """ 
        Test user fails if a user logins in with invalid credentails 
        """
        resp = self.client.post(reverse('authentication:login'), content_type='application/json',
                                data=json.dumps(self.verified_user_login_credentials))
        self.assertEqual(resp.status_code, 200)

    def test_login_with_invalid_user_fails(self):
        """ 
        Tests  return of message if a user with credentails provided is not found

        """
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

    def test_user_request_password_reset_link_succeeds(self):
        resp = self.client.post(reverse('authentication:request-password-reset'),
                                content_type='application/json',
                                data=json.dumps(
                                    self.verified_user_forgot_password)
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
                                data=json.dumps(self.invalid_user)
                                )
        self.assertDictEqual(resp.data, expected_response)

    def test_user_reset_password_valid_token(self):
        resp = self.client.post(reverse('authentication:request-password-reset'),
                                content_type='application/json',
                                data=json.dumps(
                                    self.verified_user_forgot_password)
                                )
        self.reset_password_url = parse_reset_password_url_from_body(
            mail.outbox[0].body)
        self.post_data = {
            "user": {
                "password": "New.pass.1"
            }
        }

        resp = self.client.put(self.reset_password_url, content_type='application/json',
                               data=json.dumps(self.post_data)
                               )
        self.assertEqual(resp.status_code, 200)

    def test_user_reset_password_has_valid_token_succeeds(self):
        resp = self.client.post(reverse('authentication:request-password-reset'),
                                content_type='application/json',
                                data=json.dumps(
                                    self.verified_user_forgot_password)
                                )
        self.reset_password_url = parse_reset_password_url_from_body(
            mail.outbox[0].body)
        self.post_data = {
            "user": {
                "password": "New.pass.1"
            }
        }

        resp = self.client.get(self.reset_password_url,
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_user_reset_password_has_valid_token_fails(self):
        resp = self.client.post(reverse('authentication:request-password-reset'),
                                content_type='application/json',
                                data=json.dumps(
                                    self.verified_user_forgot_password)
                                )
        self.reset_password_url_invalid = reverse(
            'authentication:password-reset', kwargs={'token': 'invalid.jwt.token'})

        resp = self.client.get(
            self.reset_password_url_invalid, content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_retrieve_user_success(self):
        """This tests for a successful retrival of a registered user"""
        response = self.client.get('/api/user/', content_type='application/json',
                                   HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        self.assertEqual("testuser", response.data["username"])

    def test_update_user_success(self):
        """This tests for a successful update of a registered user"""
        response = self.client.put('/api/user/', content_type='application/json', data=json.dumps(self.user_data),
                                   HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        self.assertEqual(3, len(response.data))


def parse_reset_password_url_from_body(body):
    urls = re.findall("(?P<url>https?://[^\s]+)", body)
    for url in urls:
        if 'password-reset' in url:
            return url[17:]+'/'
