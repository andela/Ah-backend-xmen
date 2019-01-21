import json
from rest_framework.views import status
from django.urls import reverse
from authors.apps.articles.models import Article
from authors.apps.authentication.tests_.test_base_class import BaseTestClass


class TestCreateArticleView(BaseTestClass):
    """
    Tests the Articles endpoints
    """
    def test_create_article_successfully_if_authorized(self):
        resp = self.client.post(reverse('articles:article-create'),
                                content_type='application/json',
                                data=json.dumps(self.article),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_fetch_article_succeeds_if_authorized(self):
        """
        This one checks if there is successful retrieval of articles
        """
        resp = self.client.get(reverse('articles:article-create'),
                               content_type='application/json',
                               HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_delete_an_article_succeeds_if_authorized(self):
        """
        Tests an endpoint for deleting an article
        """
        self.client.post(reverse('articles:article-create'),
                         content_type='application/json',
                         data=json.dumps(self.article),
                         HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        article = Article.objects.latest('created_at').slug
        url = reverse(
            'articles:article-update',
            kwargs={
                'slug': f'{article}'
            }
        )
        resp = self.client.delete(url, content_type='application/json',
                                  HTTP_AUTHORIZATION='Bearer ' +
                                  self.test_user_token)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_an_article_succeeds_if_authorized(self):
        """
        Tests an endpoint for updating an article
        """
        self.client.post(reverse('articles:article-create'),
                         content_type='application/json',
                         data=json.dumps(self.article),
                         HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        article = Article.objects.latest('created_at').slug
        url = reverse(
            'articles:article-update',
            kwargs={
                'slug': f'{article}'
            }
        )
        self.update_details = {
            "title": "first article",
            "description": "This is the latest description",
            "body": "This is the body of the article"
        }
        resp = self.client.put(url, data=json.dumps(self.update_details),
                               content_type='application/json',
                               HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
