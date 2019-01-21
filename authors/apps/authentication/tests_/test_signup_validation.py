import json

from django.urls import reverse
from rest_framework import status

from authors.apps.authentication.models import User
from .test_data import responses, invalid_user_data
from .test_base_class import BaseTestClass


class TestSignupValidation(BaseTestClass):
    """This class tests the functionality of the registration validation

    Examples:
    - Registration with a very short password
    - Registration with non alphanumeric password
    - Registration with an already existing email
    - Registration with an already used username
    - Registration with an invalid username

    """

    def test_signup_with_short_password_fails(self):
        """ This function tests whether the short password input from the user raises a ValidationError

        Asserts: 
            - ("Password must be longer than 8 characters."): for very short passwords
        """
        expected_response = responses['password_is_too_short']
        resp = self.client.post(reverse('authentication:signup'),
                                content_type='application/json', data=json.dumps(invalid_user_data['short_password']))
        self.assertDictEqual(resp.data, expected_response)
       
    def test_signup_with_invalid_password_fails(self):
        """ This function tests whether the non alpahnumeric password input from the user raises a ValidationError

        Asserts: 
            - ("Password should at least contain a number, capital and small letter.")

        """
        expected_response = responses['password_is_weak']
        resp = self.client.post(reverse('authentication:signup'),
                                content_type='application/json', data=json.dumps(invalid_user_data['weak_password']))
        self.assertDictEqual(resp.data, expected_response)
      

    def test_signup_with_existing_email_fails(self):
        """ This function tests that a new user cannot sign up with an existing email without raising a ValidationError

        Asserts:
            - "Email already exists."
        """
        expected_response = responses['email_already_exists']

        self.client.post(reverse('authentication:signup'),
                         content_type='application/json', data=json.dumps(self.user_data))
        resp = self.client.post(reverse('authentication:signup'),
                                content_type='application/json', data=json.dumps(invalid_user_data['same_email_user']))
        self.assertDictEqual(resp.data, expected_response)
       

    def test_signup_with_existing_username_fails(self):
        """ This function tests that a new user cannot sign up with an existing username without raising a ValidationError

        Asserts:
            - "Username already exists."
        """
        expected_response = responses['username_already_exists']
        self.client.post(reverse('authentication:signup'),
                         content_type='application/json', data=json.dumps(self.user_data))
        resp = self.client.post(reverse('authentication:signup'),
                                content_type='application/json', data=json.dumps(invalid_user_data['same_username_user']))
        self.assertDictEqual(resp.data, expected_response)
       
    def test_signup_with_invalid_username_fails(self):
        """ This function tests that a new user cannot sign up with an invalid username

        Asserts:
            - "Username can only contain letters and numbers."
        """
        expected_response = responses['invalid_username']
        resp = self.client.post(reverse('authentication:signup'),
                         content_type='application/json', data=json.dumps(invalid_user_data['invalid_username']))
        self.assertDictEqual(resp.data, expected_response)

    def test_signup_with_short_username_fails(self):
        """ This function tests that a new user cannot sign up with a short username

        Asserts:
            - "Username must be longer than 5 characters."
        """
        expected_response = responses['short_username']
        resp = self.client.post(reverse('authentication:signup'),
                         content_type='application/json', data=json.dumps(invalid_user_data['short_username']))
        self.assertDictEqual(resp.data, expected_response)

    def test_signup_with_numeric_first_character_username_fails(self):
        """ 
        This function tests that a new user cannot sign up with
        a username starting with a number

        Asserts:
            - "Username must start with a letter."
        """
        expected_response = responses['numeric_first_char_username']
        resp = self.client.post(reverse('authentication:signup'),
                         content_type='application/json', data=json.dumps(invalid_user_data['numeric_first_char_username']))
        self.assertDictEqual(resp.data, expected_response)