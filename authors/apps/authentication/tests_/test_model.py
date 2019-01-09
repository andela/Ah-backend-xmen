from authors.apps.authentication.models import User, UserManager
from django.test import TestCase


class TestModel(TestCase):
    def test_create_super_user(self):
        user = User.objects.create_superuser(username='superadmin',
                                             password='superadminpassword', email='supper@admin.com')
        self.assertEqual(user.is_staff, True)

    def test_create_user_with_no_email(self):
        with self.assertRaises(TypeError):
            user = User.objects.create_user(
                username="aggrey", email=None, password='randompassword')

    def test_create_user_with_no_username(self):
        with self.assertRaises(TypeError):
            user = User.objects.create_user(
                username=None, email='aggrey90@gmail.com', password='randompassword')

    def test_return_str__method(self):
        self.user = User.objects.create_user(
            username="aggrey", email="aggrey256@gmail.com", password='randompassword')
        self.assertEqual(self.user.__str__(), 'aggrey256@gmail.com')

    def test_return_short_name__method(self):
        self.user = User.objects.create_user(
            username="aggrey", email="aggrey256@gmail.com", password='randompassword')
        self.assertEqual('aggrey', self.user.get_short_name())

    def test_return_full_name__method(self):
        self.user = User.objects.create_user(
            username="aggrey", email="aggrey256@gmail.com", password='randompassword')
        self.assertEqual('aggrey', self.user.get_full_name)

        
