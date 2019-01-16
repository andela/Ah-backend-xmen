from django.test import TestCase
from authors.apps.notifications.models import Notification,NotificationManager
from authors.apps.profiles.models import Profile
from authors.apps.authentication.models import User
from django.urls import reverse
from .test_base_class import BaseTestClass
from django.core import mail
from rest_framework import status
import json
import time
from authors.apps.authentication.tests_ import test_data

class TestNotificationDelivery(BaseTestClass):

    def test_article_created_follower_notified_succeeds(self):
        response = self.client.post(
            f'/api/profiles/{self.test_user2.username}/follow',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        time.sleep(1)

        resp = self.client.post(reverse('authentication:login'),
                                content_type='application/json',
                                data=json.dumps(self.test_user2_login))
        self.test_user2_token = resp.data.get('token')
        
        self.assertIn('has started following', mail.outbox[0].body)
        resp = self.client.post(reverse('articles:article-create'),
                                content_type='application/json',
                                data=json.dumps(self.article),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user2_token)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        time.sleep(1)
        self.assertIn('published a new article', mail.outbox[1].body)

    
    def test_article_liked_author_notified_succeeds(self):
        resp = self.client.post(reverse('articles:article-create'),
                                content_type='application/json',
                                data=json.dumps(self.article),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token)
        article_slug = resp.data.get('slug')
        resp = self.client.post(reverse('authentication:login'),
                                content_type='application/json',
                                data=json.dumps(self.test_user2_login))
        self.test_user2_token = resp.data.get('token')

        resp = self.client.put(reverse('articles:article-likes',
                                kwargs={'slug':article_slug}),
                                content_type='application/json',
                                data=json.dumps({'like_article':True}),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user2_token)
        
        time.sleep(1)
        self.assertIn('liked your article',mail.outbox[0].body)
    
    def test_article_favorited_author_notified_succeeds(self):
        resp = self.client.post(reverse('articles:article-create'),
                                content_type='application/json',
                                data=json.dumps(self.article),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token)
        article_slug = resp.data.get('slug')
        resp = self.client.post(reverse('authentication:login'),
                                content_type='application/json',
                                data=json.dumps(self.test_user2_login))
        self.test_user2_token = resp.data.get('token')

        resp = self.client.post(reverse('articles:article-favorite',
                                kwargs={'slug':article_slug}),
                                content_type='application/json',
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user2_token)
        
        time.sleep(1)
        self.assertIn('favorited your article',mail.outbox[0].body)
    def test_article_commented_favorites_notified_succeeds(self):
        """ 
        When user1 creates an article, then user2 favorites it, 
        user2 receives notifications about a comment from user3
        """
        resp = self.client.post(reverse('articles:article-create'),
                                content_type='application/json',
                                data=json.dumps(self.article),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token)
        article_slug = resp.data.get('slug')
        resp = self.client.post(reverse('authentication:login'),
                                content_type='application/json',
                                data=json.dumps(self.test_user2_login))
        self.test_user2_token = resp.data.get('token')

        resp = self.client.post(reverse('articles:article-favorite',
                                kwargs={'slug':article_slug}),
                                content_type='application/json',
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user2_token)
                                
        resp = self.client.post(reverse('authentication:login'),
                                content_type='application/json',
                                data=json.dumps(self.test_user3_login))
        self.test_user3_token = resp.data.get('token')
        resp=self.client.post(reverse('comments:comments',args=[article_slug]),
                                        content_type='application/json',
                                        HTTP_AUTHORIZATION='Bearer ' +
                                        self.test_user3_token,
                                        data=json.dumps(test_data.comment_data['comment_data']))

       
        time.sleep(1)
        self.assertIn(
            'left a  comment on an article you favorited',
            mail.outbox[2].body
            )


    def test_comment_created_author_notified_fails(self):
        resp = self.client.post(reverse('articles:article-create'),
                                content_type='application/json',
                                data=json.dumps(self.article),
                                HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token)
        article_slug = resp.data.get('slug')
        resp=self.client.post(reverse('comments:comments',args=[article_slug]),
                                        content_type='application/json',
                                        HTTP_AUTHORIZATION='Bearer ' +
                                        self.test_user_token,
                                        data=json.dumps(test_data.comment_data['comment_data']))

        self.assertEqual(resp.status_code,201)
        time.sleep(1)
        self.assertEqual(0,len(mail.outbox))
