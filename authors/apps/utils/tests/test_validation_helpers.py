from authors.apps.utils.validators import validation_helpers
from rest_framework import serializers
from django.test import TestCase


class TestModel(TestCase):
    def test_validate_password_fails(self):
        with self.assertRaises(serializers.ValidationError):
            password = validation_helpers.validate_password(None)
        with self.assertRaises(serializers.ValidationError):
            password = validation_helpers.validate_password('')
        with self.assertRaises(serializers.ValidationError):
            password = validation_helpers.validate_password('123456qwe')
    
    def test_validate_password_succeeds(self):
        password = validation_helpers.validate_password('Strong.Password.2')
        self.assertEqual(password,'Strong.Password.2')        
    