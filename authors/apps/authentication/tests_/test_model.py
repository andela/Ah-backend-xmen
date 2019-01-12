from authors.apps.authentication.models import User, UserManager
from django.test import TestCase


class TestModel(TestCase):

    def test_create_super_user_with_no_password_fail(self):
        """
        Test raise error if a superuser is created without a password

        Returns:
            A message that password is required
        Raises:
            TypeError if password is not provided
        """
        with self.assertRaises(TypeError):
            user = User.objects.create_superuser(username='superadmin',
                                                 password=None, email='supper@admin.com')

    def test_create_super_user(self):
        """
        Test successful creation of a superuser

        Returns:
            A superuser should have is.staff set to true

        """
        user = User.objects.create_superuser(username='superadmin',
                                             password='superadminpassword', email='supper@admin.com')
        self.assertEqual(user.is_staff, True)

    def test_create_user_with_no_email(self):
        """
        Test raise error if a user is created without an email

        Returns:
            A message that email is required
        Raises:
            TypeError if email is not provided
        """

        with self.assertRaises(TypeError):
            user = User.objects.create_user(
                username="aggrey", email=None, password='randompassword')

    def test_create_user_with_no_username(self):
        """
        Test raise error if a user is created without an username

        Returns:
            A message that username is required
        Raises:
            TypeError if username is not provided
        """
        with self.assertRaises(TypeError):
            user = User.objects.create_user(
                username=None, email='aggrey90@gmail.com', password='randompassword')

    def test_return_str__method(self):
        """
        Test __str__ method on user model

        Returns:
            when __str__ is called is should return a users email

        """
        self.user = User.objects.create_user(
            username="aggrey", email="aggrey256@gmail.com", password='randompassword')
        self.assertEqual(self.user.__str__(), 'aggrey256@gmail.com')

    def test_return_short_name__method(self):
        """
        Test get_short_name method on user model

        Returns:
            when get_short_name is called is should return a users username

        """
        self.user = User.objects.create_user(
            username="aggrey", email="aggrey256@gmail.com", password='randompassword')
        self.assertEqual('aggrey', self.user.get_short_name())

    def test_return_full_name__method(self):
        """
        Test get_full_name method on user model

        Returns:
            when get_full_name is called is should return a users username

        """
        self.user = User.objects.create_user(
            username="aggrey", email="aggrey256@gmail.com", password='randompassword')
        self.assertEqual('aggrey', self.user.get_full_name)
