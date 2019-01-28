import json
from authors.apps.authentication.tests_.test_base_class import BaseTestClass
from rest_framework import status


class TestUserProfile(BaseTestClass):

    

    def test_retrieve_profile_with_valid_token_succeeds(self):
        """
        Args:
          username: (Django Model instance)
          user_token: (Authentication credentials)

          Returns a user profile if the token is valid and the user
          exists in the database
        """
        response = self.client.get(
            f'/api/profiles/{self.test_user.username}',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('testuser', response.data['username'])

    def test_retrieve_profile_without_logging_in_fails(self):
        """
        Args:
           username: (Django model instance)
        
        Raises:
             Django HTTP_FORBIDDEN exception (Django request)
        """
        response = self.client.get(f'/api/profiles/{self.test_user.username}',
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_my_profile_succeeds(self):
        """
        Args:
           username:
           user_token (User credentials)

        Returns:
           JSON response of updated details on success
        """
        response = self.client.put(
            f'/api/profiles/{self.test_user.username}/edit',
            content_type='application/json',
            data=json.dumps(self.update_data),
            HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_view_author_profiles_succeeds(self):
        """
        Expects:
           user_token
        
        Returns:
            List of existing user profiles: (Django HTTP Response)
        """
        response = self.client.get(f'/api/profiles/',
                  HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authenticated_user_view_author_profiles_fails(self):
        """
        Raises:
           Request forbidden exception (Django http exception)
        """
        response = self.client.get(f'/api/profiles/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_loggedin_user_views_favorite_articles_succeeds(self):
        response = self.client.get(f'/api/profiles/', HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
