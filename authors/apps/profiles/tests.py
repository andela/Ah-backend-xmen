import json
from authors.apps.authentication.tests_.test_base_class import BaseTestClass
from rest_framework import status


class TestUserProfile(BaseTestClass):

    def test_retrieve_profile_with_valid_token_succeeds(self):
        response = self.client.get(
            f'/api/profiles/{self.test_user.username}',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('testuser', response.data['username'])

    def test_retrieve_profile_without_logging_in_fails(self):
        response = self.client.get(f'/api/profiles/{self.test_user.username}',
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_my_profile_succeeds(self):
        response = self.client.put(
            f'/api/profiles/{self.test_user.username}/edit',
            content_type='application/json',
            data=json.dumps(self.update_data),
            HTTP_AUTHORIZATION='Bearer ' + self.test_user_token
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
