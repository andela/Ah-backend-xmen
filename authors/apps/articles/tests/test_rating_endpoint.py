import json
from rest_framework.views import status
from django.urls import reverse
from authors.apps.authentication.tests_.test_base_class import BaseTestClass


class TestRateArticleView(BaseTestClass):
    """
    Tests the Rating Articles endpoint
    """

    def test_rate_article_succeeds(self):
        resp = self.client.post(self.rate_url,
                                content_type='application/json',
                                data=json.dumps(self.test_valid_rating),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_already_rated_article_succeeds(self):
        """
        This tests if the user has already rated the same article
        """
        self.client.post(self.rate_url,
                         content_type='application/json',
                         data=json.dumps(self.test_valid_rating),
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.test_user_token)
        resp = self.client.post(self.rate_url,
                                content_type='application/json',
                                data=json.dumps(self.test_valid_rating),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token)
        self.assertIn("You have already rated the article",
                      resp.data.get('message'))

    def test_get_average_rating_success(self):
        """
        Tests the value of average ratings
        """
        self.client.post(self.rate_url,
                         content_type='application/json',
                         data=json.dumps(self.test_valid_rating),
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.test_user_token)
        resp = self.client.get(self.single_article_url,
                               content_type='application/json',
                               HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token)
        self.assertEqual(3, resp.data.get('average_rating'))
