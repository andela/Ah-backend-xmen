from django.test import TestCase
from authors.apps.authentication.models import User
from rest_framework.test import APIClient
from django.urls import reverse
import json
from authors.apps.profiles.models import Profile
from authors.apps.articles.models import Article
from authors.apps.authentication.tests_ import test_data
from authors.apps.comments.models import Comment,CommentReply
from decouple import config
import jwt


class BaseTestClass(TestCase):
    def setUp(self):
        self.user_data = {
            "user": {
                "username": "Jacob",
                "email": "jake@jake.jake",
                "password": "JakeJake12"
            }
        }
        self.user_data_weak_password = {
            "user": {
                "username": "Jacob",
                "email": "jake@jake.jake",
                "password": "jakejake"
            }
        }
        self.user_data_short_password = {
            "user": {
                "username": "Jacob",
                "email": "jake@jake.jake",
                "password": "jake"
            }
        }
        self.user2_data = {
            "user": {
                "username": "Jacob1",
                "email": "jake1@jake.jake",
                "password": "JakeJake12"
            }
        }
        self.update_data = {
            "first_name": "Soultech",
            "last_name": "Muhwezi",
            "bio": "Sample bio data"
        }
        self.same_email_user = {
            "user": {
                "username": "Jackson",
                "email": "jake@jake.jake",
                "password": "jAckson5"
            }
        }
        self.same_username_user = {
            "user": {
                "username": "Jacob",
                "email": "jake@gmail.com",
                "password": "jAcobson10"
            }
        }
        self.verified_user = User.objects.create_user(
            username='testuser1',
            email='testemail1@test.com',
            password='testpassworD12')

        self.verified_user_login_credentials = {
            "user": {
                "email": "testemail@test.com",
                "password": "testpassworD12"
            }
        }

        self.verified_user2_login_credentials = {
            "user": {
                "email": "soultechdev@gmail.com",
                "password": "testpassworD12"
            }
        }

        self.verified_user_forgot_password = {
            "user": {
                "email": "testemail@test.com"
            }
        }
        self.invalid_user = {
            "user": {
                "email": "adddd@gmail.com",
                "password": "Aaddadasas"

            }
        }
        
      
        self.client = APIClient()
        self.test_user = User.objects.create_user(
            username='testuser',
            email='testemail@test.com', password='testpassworD12')
        self.test_user2 = User.objects.create_user(
            username='soultech',
            email='soultechdev@gmail.com',
            password='testpassworD12'
        )
        

        self.client = APIClient()
        sign_up_response = self.client.post(reverse('authentication:login'),
                                            content_type='application/json', data=json.dumps(self.verified_user_login_credentials))
        signup2 = self.client.post(reverse('authentication:login'),
                                            content_type='application/json', data=json.dumps(self.verified_user2_login_credentials))

        self.test_user_token = sign_up_response.data['token']
        self.alt_test_user_token = signup2.data.get('token')


        self.not_author_user=User.objects.create_user(
            username='notauthor',
            password="NotAuthoruser12",
            email='notauthor@author.com'
        )

        self.not_author_user_login_reponse=self.client.post(reverse('authentication:login'), content_type='application/json', data=json.dumps(
                                                test_data.invalid_user_data['not_author_login_credentials']
                                            ))
    
        self.not_author_token=self.not_author_user_login_reponse.data['token']

        self.article = {
            "title": "hello worlfd",
            "description": "desctriptuo",
            "body": 'boddydydabagd',
            "tags": ["andela", "xmen"]
        }
        self.profile=Profile.objects.get(user=self.verified_user)
        self.created_article=Article.objects.create(
            body=' hello world',description='a description',
            title='a title',author=self.profile
        )

        self.testcomment=Comment.objects.create(body='a test comment body',author=self.profile,article=self.created_article)
        self.testCommentReply=CommentReply.objects.create(reply_body='a test reply body',comment=self.testcomment,author=self.profile)

        self.create_article_response = self.client.post(
            reverse('articles:article-create'),
            content_type='application/json',
            data=json.dumps(self.article),
            HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        test_article = Article.objects.latest('created_at').slug
        self.single_article_url = reverse(
            'articles:article-update',
            kwargs={
                'slug': f'{test_article}'
            }
        )
        self.like_url = reverse(
            'articles:article-likes',
            kwargs={
                'slug': f'{test_article}'
            }
        )
        self.rate_url = reverse(
            'articles:article-rates',
            kwargs={
                'slug': f'{test_article}'
            }
        )
        self.like_request = {
            "like_article": True
        }

        self.dislike_request = {
            "like_article": False
        }

        # Tokens to be used for the social platforms
        # Facebook authorisation tokens
        self.valid_facebook_token = {
            "auth_token": config('auth_token')
        }
        self.invalid_facebook_token = {
            "auth_token": "hjdwheugclaugiehuyegcuehugcyegaehcgygeiouegfhuiwygauyesfidghc"
        }
        #Twitter authorization tokens 
        self.invalid_twitter_tokens = {
            "access_token": "hjdwheugclaugiehkjhgdshggdgg.lkjhugcyegaehcgyge",
            "access_token_secret": "ksuyfdxzsjhfxyashdchlxahkcgyfudc"
        }
        self.valid_twitter_tokens = {
            "access_token": config('access_token'),
	        "access_token_secret": config('access_token_secret')
        }
        #Google authorization tokens 
        self.invalid_google_token = {
            "access_token": "hjdwheugclaugiehkjhgdshggdgg.lkjhugcyegaehcgygebkjbcbjkbjc"
        }
        self.valid_google_token = {
            "auth_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjA4ZDMyNDVjNjJmODZiNjM2MmFmY2JiZmZlMWQwNjk4MjZkZDFkYzEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDk1Mzk3ODQ5NDg3MzM1NzYyMzUiLCJlbWFpbCI6ImRvdWdsYXMua2F0bzdAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJ1Vmh0V2RlWUNOeFFpU3BNT3BvYW9BIiwibmFtZSI6IkRvdWdsYXMgS2F0byIsInBpY3R1cmUiOiJodHRwczovL2xoNC5nb29nbGV1c2VyY29udGVudC5jb20vLXU5WTQxT3V5b0VRL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFjL0xlWTFNbmtRV0tFL3M5Ni1jL3Bob3RvLmpwZyIsImdpdmVuX25hbWUiOiJEb3VnbGFzIiwiZmFtaWx5X25hbWUiOiJLYXRvIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE1NDgyMzYyNjMsImV4cCI6MTU0ODIzOTg2M30.U3kSajYGNmHncTNhck5ECpgNxj-bcbA8wjqw1dUVrYr6W3UMVRS72Bm8758rgLHoFonSKbTLTeM5LuZcD6KFmJCDoaPJlSilwJySkKZCsPggQ3feL9UGskFoqYT6EIMm78_8UW1svwbmVu7WXsBG9j4RdwCwFiXEfdmaVNQimUtj7xxqgUaW43ftGA2lQi1uqcuIueHi9YpB0glMDJMEZ1QbJxYd_lx6lbubei6sg3fScP2Y2qo0c71TeZp3P652Rwb8vmuGwZ0m5vehbRxzE_I6q9SGWqfMkHbOe8Zpef6U-dk4G3AQCKJK689TWNQDmWo-Je8R3mrT_vvbNbC28w"
        }
        self.test_profile = {
            'name': 'profile.name',
            'email': 'profile.email'
        }
        self.test_valid_rating = {
            'rating': 3
        }
        decoded_token = jwt.decode(self.test_user_token, None, None)
        self.test_author = (decoded_token['user_data'].split(" ")[1])
