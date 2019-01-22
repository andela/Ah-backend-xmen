from django.test import TestCase
from authors.apps.authentication.models import User
from rest_framework.test import APIClient
from django.urls import reverse
import json
from authors.apps.profiles.models import Profile
from authors.apps.articles.models import Article
from authors.apps.authentication.tests_ import test_data
from authors.apps.comments.models import Comment
class BaseTestClass(TestCase):
    def setUp(self):
        self.user_data = {
            "user": {
                "username": "Jacob",
                "email": "jake@jake.jake",
                "password": "JakeJake12"
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
        

        sign_up_response = self.client.post(reverse('authentication:login'),
                                            content_type='application/json', data=json.dumps(self.verified_user_login_credentials))

        self.test_user_token = sign_up_response.data['token']

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
            "body": 'boddydydabagd'
        }
        self.profile=Profile.objects.get(user=self.verified_user)
        self.created_article=Article.objects.create(
            body=' hello world',description='a description',
            title='a title',author=self.profile
        )

        self.testcomment=Comment.objects.create(body='a test comment body',author=self.profile,article=self.created_article)
        
