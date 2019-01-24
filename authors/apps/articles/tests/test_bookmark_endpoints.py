import json
from rest_framework.views import status
from django.urls import reverse
from authors.apps.articles.models import Article
from authors.apps.authentication.tests_.test_base_class import BaseTestClass


class TestBookmarkArticlesView(BaseTestClass):
    """
    Tests the bookmark endpoints endpoints
    """
    def _make_request(self,method):
        if method == 'delete':
            return self.client.delete(reverse('articles:article-bookmark',
                                 kwargs=self.kwargs),
                                content_type='application/json',
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token)
        elif method == 'post':
            return self.client.post(reverse('articles:article-bookmark',
                                 kwargs=self.kwargs),
                                content_type='application/json',
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token)

    def _make_toggle_request_unauthorized(self):
        return self.client.put(reverse('articles:article-bookmark',
                                 kwargs=self.kwargs),
                                content_type='application/json')
    def test_bookmark_article_unauthorized_fails(self):
        self.add_demo_article()
        resp = self._make_toggle_request_unauthorized()
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('credentials were not provided', resp.data.get('detail'))

    def test_post_bookmark_article_succeeds(self):
        self.add_demo_article()
        resp = self._make_request('post')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('added to bookmarks', resp.data.get('message'))

        resp = self._make_request('post')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    def test_delete_bookmark_article_succeeds(self):
        self.add_demo_article()
        resp = self._make_request('post')
        resp = self._make_request('delete')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('removed from bookmarks', resp.data.get('message'))

        resp = self._make_request('delete')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fetch_bookmarks_succeeds(self):
        self.add_demo_article()
        resp = self._make_request('post')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('added to bookmarks', resp.data.get('message'))

        resp = self.client.get(reverse('bookmarks'),
                                content_type='application/json',
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(resp.data))

  
    def add_demo_article(self):    
        self.client.post(reverse('articles:article-create'),
                                content_type='application/json',
                                data=json.dumps(self.article),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token)
        self.kwargs = {
            'slug': Article.objects.latest('created_at').slug
            }
        

   