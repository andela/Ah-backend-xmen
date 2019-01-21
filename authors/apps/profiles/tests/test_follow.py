import json
from authors.apps.profiles.tests.test_base_class import BaseTestClass
from rest_framework import status
from authors.apps.profiles.models import Profile, ProfileManager
from authors.apps.profiles.apps import ProfilesConfig

class TestUserFollow(BaseTestClass):

    def test_profiles_app_instance(self):
        self.assertEqual(ProfilesConfig.name, "profiles")

    def test_follow_user_succeeds(self):
        response = self.client.post(
            f'/api/profiles/{self.user2.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_unfollow_user_succeeds(self):
        self.client.post(
            f'/api/profiles/{self.user2.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.delete(
            f'/api/profiles/{self.user2.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)   
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_self_fails(self):
        response = self.client.post(
            f'/api/profiles/{self.user1.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_list_of_followers_succeeds(self):
        self.client.post(
            f'/api/profiles/{self.user2.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(
            f'/api/profiles/{self.user2.username}/followers',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_return_list_of_following_succeeds(self):
        self.client.post(
            f'/api/profiles/{self.user2.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(
            f'/api/profiles/{self.user1.username}/following',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_return_number_of_following_succeeds(self):
        self.client.post(
            f'/api/profiles/{self.user2.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(
            f'/api/profiles/{self.user1.username}',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_number_of_followers_succeeds(self):
        self.client.post(
            f'/api/profiles/{self.user2.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(
            f'/api/profiles/{self.user2.username}',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_if_user_is_following_another_succeeds(self):
        self.client.post(
            f'/api/profiles/{self.user2.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(
            f'/api/profiles/{self.user2.username}',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_if_user_is_not_following_another_succeeds(self):
        response = self.client.get(
            f'/api/profiles/{self.user2.username}',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_non_existent_user_fails(self):
        response = self.client.post(
            f'/api/profiles/jane/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_follow_already_followed_user_fails(self):
        self.client.post(
            f'/api/profiles/{self.user2.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.post(
            f'/api/profiles/{self.user2.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)   
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_already_unfollowed_user_fails(self):
        self.client.post(
            f'/api/profiles/{self.user2.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        self.client.delete(
            f'/api/profiles/{self.user2.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token) 
        response = self.client.delete(
            f'/api/profiles/{self.user2.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)    
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_self_fails(self):
        response = self.client.delete(
            f'/api/profiles/{self.user1.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
