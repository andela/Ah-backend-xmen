import json
from rest_framework.views import status
from django.urls import reverse
from authors.apps.articles.models import Article
from authors.apps.authentication.tests_.test_base_class import BaseTestClass
from authors.apps.authentication.tests_.test_data import responses, invalid_request_data


class TestTagListAPIView(BaseTestClass):
    """
    Checks for the get all tags endpoint
    """
    def test_fetch_all_tags_succeeds_if_authorized(self):
        """
        Testing if there is successful retrieval of all tags
        """
        response = self.client.get(reverse('tags'),
                        HTTP_AUTHORIZATION='Bearer ' +
                        self.test_user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
