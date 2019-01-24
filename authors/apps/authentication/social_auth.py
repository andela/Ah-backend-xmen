import os
import facebook
import twitter
from google.oauth2 import id_token
from decouple import config
from rest_framework import status
from rest_framework.response import Response
from google.auth.transport import requests


class SocialAuth:

    @staticmethod
    def verify_facebook_token(auth_token):
        """
        This verify facebook token class handles both verifying and decoding of the token
        acquired from the facebook GraphAPI and then returns the facebook user
        """
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            facebook_profile = graph.request('/me?fields=name,email')
            return facebook_profile
        except facebook.GraphAPIError as e:
            pass
        
    @staticmethod
    def verify_google_token(auth_token):
        """
        Here there is validation and verification of the token and then decoding from google
        class handles both verifying and decoding of the token
        acquired from the google developer account and then returns the google user
        """
        try:
            google_profile = id_token.verify_oauth2_token(auth_token, requests.Request())
            return google_profile
        except Exception as e:
            pass

    @staticmethod
    def verify_twitter_token(api_key, api_secret_key):
        """
        Validating, verifying of the token and then decoding from google
        class handles both verifying and decoding of the token
        acquired from the google developer account and then returns the google user
        """
        consumer_key = config('TWITTER_CONSUMER_API_KEY')
        consumer_secret = config('TWITTER_CONSUMER_SECRET_KEY')

        try:
            api=twitter.Api(
                    consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token_key=api_key,
                    access_token_secret=api_secret_key
                )
            twitter_profile = api.VerifyCredentials(include_email=True)
            return twitter_profile
        except Exception as e:
            pass
