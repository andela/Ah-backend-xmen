import json
from rest_framework.views import status
from django.urls import reverse
from authors.apps.articles.models import Article, ReadStats
from authors.apps.authentication.tests_.test_base_class import BaseTestClass
from authors.apps.authentication.tests_.test_data import (
    responses, invalid_request_data, report_data
)
from authors.apps.articles.apps import ArticlesConfig



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

    def test_add_read_stats_succeeds(self):
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
        resp = self.client.get(url,
                               HTTP_AUTHORIZATION='Bearer ' +
                               self.not_author_token)
        self.assertEqual(resp.status_code, 200)


    def test_filter_article_by_author_succeeds(self):
        self.client.post(reverse('articles:article-create'),
                         content_type='application/json',
                         data=json.dumps(self.article),
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.test_user_token)

        resp = self.client.get(reverse('articles:article-create') + '?author='
                               + self.test_author,
                               content_type='application/json',
                               HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_filter_by_title_succeeds(self):
        self.client.post(reverse('articles:article-create'),
                         content_type='application/json',
                         data=json.dumps(self.article),
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.test_user_token)
        title = self.article['title']
        resp = self.client.get(reverse('articles:article-create') + '?title='
                               + title,
                               content_type='application/json',
                               HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_favorites_filter_succeeds(self):
        """
        favorites filter is based on the Article manager model
        """
        self.client.post(reverse('articles:article-create'),
                         content_type='application/json',
                         data=json.dumps(self.article),
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.test_user_token)
        article = Article.objects.latest('created_at').slug
        self.client.post(f'/api/articles/{article}/favorite',
                         HTTP_AUTHORIZATION=f'Bearer {self.test_user_token}')
        value = True
        resp = self.client.get(f'/api/articles/?favorited={value}',
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    
    def test_filter_article_by_tags_succeeds(self):
        """
        Tests that filters by tag succeeds
        """
        self.client.post(reverse('articles:article-create'),
                         content_type='application/json',
                         data=json.dumps(self.article),
                         HTTP_AUTHORIZATION='Bearer ' +
                         self.test_user_token)
        tag = self.article['tags'][1]
        resp = self.client.get(reverse('articles:article-create') + '?tags='
                               + tag,
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

    def test_unlike_article_fails_if_user_has_not_liked_article(self):
        rep=self.client.post(reverse('articles:article-create'),
                         content_type='application/json',
                         data=json.dumps(self.article),
                         HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        article_slug=rep.data['slug']

        rep=self.client.delete(reverse('articles:article-likes',args=[article_slug]),
            HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        self.assertEqual(rep.status_code,400)

    def test_favoriting_an_article_succeeds_if_authorized(self):
        """
        Checks if an authenticated user can favortie an article
        If the article has been favorited, it is removed from favorites
        Args: slug (Django model article instance)
        
        Returns  response (Django HTTP Response)
        """
        self.client.post(reverse('articles:article-create'),
                         content_type='application/json',
                         data=json.dumps(self.article),
                         HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        article = Article.objects.latest('created_at').slug
        response = self.client.post(
            f'/api/articles/{article}/favorite',
            HTTP_AUTHORIZATION=f'Bearer {self.test_user_token}'
        )
        response2 = self.client.delete(
            f'/api/articles/{article}/favorite',
            HTTP_AUTHORIZATION=f'Bearer {self.test_user_token}'
        )
        self.assertIn('Article has been removed from favorites', response2.data.get('message'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unfavoriting_an_article_fails_if_not_in_favorites(self):
        """
        Checks if an authenticated user can favorite an article
        If the article has been favorited, it is removed from favorites
        Otherwise the user is notified that such an article doesnot
        exist in their favorites list.
        
        Args: slug (Django model article instance)
        
        Returns  response (Django HTTP Response)
        """
        self.client.post(reverse('articles:article-create'),
                         content_type='application/json',
                         data=json.dumps(self.article),
                         HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        article = Article.objects.latest('created_at').slug
        response = self.client.post(
            f'/api/articles/{article}/favorite',
            HTTP_AUTHORIZATION=f'Bearer {self.test_user_token}'
        )
        response2 = self.client.delete(
            f'/api/articles/{article}/favorite',
            HTTP_AUTHORIZATION=f'Bearer {self.test_user_token}'
        )
        response3 = self.client.delete(
            f'/api/articles/{article}/favorite',
            HTTP_AUTHORIZATION=f'Bearer {self.test_user_token}'
        )
        self.assertIn('Article does not exist in your favorites', response3.data.get('message'))

    def test_favoriting_twice_fails(self):
        """
        Checks if an authenticated user can favortie an article
        If the article has been favorited, the user is notified that they have
        already added that article top their favorites list.
        Args: slug (Django model article instance)
        
        Returns  response (Django HTTP Response)
        """
        self.client.post(reverse('articles:article-create'),
                         content_type='application/json',
                         data=json.dumps(self.article),
                         HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        article = Article.objects.latest('created_at').slug
        response = self.client.post(
            f'/api/articles/{article}/favorite',
            HTTP_AUTHORIZATION=f'Bearer {self.test_user_token}'
        )
        response2 = self.client.post(
            f'/api/articles/{article}/favorite',
            HTTP_AUTHORIZATION=f'Bearer {self.test_user_token}'
        )
        self.assertIn('Article already in favorites', response2.data.get('message'))

    def test_authenticated_user_fetch_favorite_article_succeeds(self):
        """
        Checks if an authenticated user can view a list of favorited articles

        Returns  response (Django HTTP Response)
        """
        self.client.post(reverse('articles:article-create'),
                         content_type='application/json',
                         data=json.dumps(self.article),
                         HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        article = Article.objects.latest('created_at').slug
        self.client.post(
            f'/api/articles/{article}/favorite',
            HTTP_AUTHORIZATION=f'Bearer {self.test_user_token}'
        )
        response2 = self.client.get(
            f'/api/articles/favorites',
            HTTP_AUTHORIZATION=f'Bearer {self.test_user_token}'
        )
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_articles_app_instance(self):
        self.assertEqual(ArticlesConfig.name, 'articles')

    def test_reporting_your__on_own_article_fails(self):
        """
        Checks if an authenticated user can favortie an article
        If the article has been favorited, the user is notified that they have
        already added that article top their favorites list.
        Args: slug (Django model article instance)
        
        Returns  response (Django HTTP Response)
        """
        self.client.post(reverse('articles:article-create'),
                         content_type='application/json',

                         HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        article = Article.objects.latest('created_at').slug
        data = {
            "reason":"Explicit content"
        }
        response2 = self.client.post(
            f'/api/articles/{article}/report',
            content_type='application/json',
            data=json.dumps(data),
            HTTP_AUTHORIZATION=f'Bearer {self.test_user_token}')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('You do not have permission to perform this action', response2.data.get('detail'))

    def test_reporting_on_another_author_article_succeeds(self):
        """
        Checks if an authenticated user can report an article
        If the user is not the author, the article is reported to 
        the admins
        Args: slug (Django model article instance)
        
        Returns  response (Django HTTP Response)
        """
        self.client.post(reverse('articles:article-create'),
                         content_type='application/json',

                         HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        article = Article.objects.latest('created_at').slug
        data = {
            "reason":"Explicit content"
        }
        response2 = self.client.post(
            f'/api/articles/{article}/report',
            content_type='application/json',
            data=json.dumps(data),
            HTTP_AUTHORIZATION=f'Bearer {self.alt_test_user_token}')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
  

class TestReadStatsView(BaseTestClass):

    def test_fetch_read_stats_succeeds_if_authorized(self):
        """
        Checking if there is successful retrieval of the read_stats
        Args:
           token: (generated token after login)
        Raises:
             Django HTTP_FORBIDDEN exception (Django request)
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
        resp = self.client.get(url,
                               HTTP_AUTHORIZATION='Bearer ' +
                               self.not_author_token)
        self.assertEqual(resp.status_code, 200)
        resp=self.client.get(reverse("profiles:read-stats",args=[self.not_author_user.username]),
            HTTP_AUTHORIZATION='Bearer ' +
                             self.not_author_token
        )
        self.assertEqual(resp.status_code,200)

    def test_str_method_for_read_stats(self):
        """
        Tests that __str__ generates a correct string 
        representation of a read stat 
        """
        reading_stats = ReadStats.objects.create(article=self.created_article,user=self.test_user,read_stats=1)
        self.assertEqual(reading_stats.__str__(),'article_title: a title, user: testemail@test.com, read_stats: 1')

    def test_fetching_all_read_stats_without_permission(self):
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
        resp = self.client.get(url,
                               HTTP_AUTHORIZATION='Bearer ' +
                               self.not_author_token)
        resp=self.client.get(reverse("profiles:read-stats",args=[self.not_author_user.username]),
            HTTP_AUTHORIZATION='Bearer ' +
                             self.test_user_token
        )
        self.assertIn('You dont have the permissions to access this route',str(resp.data))
        