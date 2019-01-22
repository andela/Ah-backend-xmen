import json
from rest_framework.views import status
from django.urls import reverse
from authors.apps.articles.models import Article
from authors.apps.authentication.tests_.test_base_class import BaseTestClass
from authors.apps.authentication.tests_.test_data import responses, invalid_request_data


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


class ArticleLikeView(BaseTestClass):

    def test_like_an_article_fails(self):
        """Tests the like-dislike endpoint with no request data"""
        response = self.client.put(
            self.like_url,
            content_type='application/json',
            data=json.dumps(invalid_request_data['no_request_body']),
            HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        expected_response = responses['no_request_body']
        self.assertDictEqual(response.data, expected_response)

    def test_like_an_article_another_fails(self):
        """Tests the like-dislike endpoint using none boolean request value"""
        response = self.client.put(
            self.like_url,
            content_type='application/json',
            data=json.dumps(invalid_request_data['none_boolean']),
            HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        expected_response = responses['none_boolean']
        self.assertDictEqual(response.data, expected_response)

    def test_like_an_article_succeeds(self):
        """Tests an endpoint that likes an article"""
        response = self.client.put(
            self.like_url,
            content_type='application/json',
            data=json.dumps(self.like_request),
            HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        self.assertIn("You have liked an article", response.data["message"])

    def test_like_after_like_succeeds(self):
        """like an already liked article by the same user"""
        self.client.put(
            self.like_url,
            content_type='application/json',
            data=json.dumps(self.like_request),
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        response = self.client.put(
            self.like_url,
            content_type='application/json',
            data=json.dumps(self.like_request),
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        self.assertIn("You have already liked the article",
                      response.data["message"])

    def test_unlike_an_article_succeeds(self):
        """Unlike an already liked article by the same user"""
        self.client.put(
            self.like_url,
            content_type='application/json',
            data=json.dumps(self.like_request),
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        response = self.client.delete(
            self.like_url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        self.assertIn("You have unliked an article", response.data["message"])

    def test_dislike_an_article_succeeds(self):
        """Tests an endpoint that dislikes an article"""
        response = self.client.put(
            self.like_url,
            content_type='application/json',
            data=json.dumps(self.dislike_request),
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        self.assertIn("You have disliked an article", response.data["message"])

    def test_dislike_after_dislike_succeeds(self):
        """Dislike an already disliked article by the same user"""
        self.client.put(
            self.like_url,
            content_type='application/json',
            data=json.dumps(self.dislike_request),
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        response = self.client.put(
            self.like_url,
            content_type='application/json',
            data=json.dumps(self.dislike_request),
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        self.assertIn("You have already disliked the article",
                      response.data["message"])

    def test_undislike_an_article_succeeds(self):
        """Remove a dislike from a disliked article by the same user"""
        self.client.put(
            self.like_url,
            content_type='application/json',
            data=json.dumps(self.dislike_request),
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        response = self.client.delete(
            self.like_url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        self.assertIn("You have un-disliked an article",
                      response.data["message"])

    def test_like_after_dislike_an_article_succeeds(self):
        """like a formerly a disliked article by the same user"""
        self.client.put(
            self.like_url,
            content_type='application/json',
            data=json.dumps(self.dislike_request),
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        response = self.client.put(
            self.like_url,
            content_type='application/json',
            data=json.dumps(self.like_request),
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        self.assertIn("You have liked an article", response.data["message"])

    def test_dislike_after_like_an_article_succeeds(self):
        """Dislike a formerly a liked article by the same user"""
        self.client.put(
            self.like_url,
            content_type='application/json',
            data=json.dumps(self.like_request),
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        response = self.client.put(
            self.like_url,
            content_type='application/json',
            data=json.dumps(self.dislike_request),
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        self.assertIn("You have disliked an article", response.data["message"])

    def test_list_of_users_liked_succeeds(self):
        """Tests an endpoint that lists users that liked/disliked"""
        self.client.put(
            self.like_url,
            content_type='application/json',
            data=json.dumps(self.like_request),
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        response = self.client.get(
            self.like_url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        self.assertListEqual(["testuser"],
                             response.data.get("likes"))
