from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from authors.apps.core.models import PasswordResetManager
from .backends import JWTAuthentication

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    PasswordResetRequestSerializer, PasswordResetSerializer,
    FacebookSocialAuthSerializer, GoogleSocialAuthSerializer,
    TwitterSocialAuthSerializer
)
from .utils import email_verification_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from datetime import datetime
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import quote

import facebook
from .social_auth import SocialAuth
import uuid


class RegistrationAPIView(GenericAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        """
        Send user an email verification to the email they registered with.
        
        Returns:
            A success message is returned to the user and a verification is sent to the email they 
            registered with
        Raises:
            serializer.ValidationErrors: if user provides invalid data or tries to register with data 
            of an existing user
        
        """
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        uuid = urlsafe_base64_encode(
            force_bytes(user.pk)).decode()
        token = email_verification_token.make_token(user)
        subject = "Email Verification For Authors Heaven"
        email_verification_url = reverse(
            'authentication:email-verification', args=[uuid, token])
        url = request.build_absolute_uri(email_verification_url)
        context = {'username': user.username,
                   'url': url}

        message_string = render_to_string('email.html', context,)
        reciever_email = user.email
        send_mail(subject, message_string,
                  'admin@authorshaven', [reciever_email, ])

        return Response({'message':
                         "An email verification link has been sent to to {} please click the link to confirm your email".format(reciever_email), 
                         "Info": serializer.data}, status=status.HTTP_201_CREATED)


class EmailVerificationAPIView(GenericAPIView):
    def get(self, request, uuid, token):
        try:
            user_id = force_bytes(urlsafe_base64_decode(uuid)).decode('utf-8')
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist as e:
            front_end_url = settings.FRONTEND_BASE_URL + '/signup/'+quote(str(e))
            return redirect(front_end_url)
        
        if user is not None and email_verification_token.check_token(user, token):
            user.email_verified = True
            user.email_verification_date = datetime.utcnow()
            user.save()
            message = 'Email verification for {} was completed succesfully'.format(user.email)
            front_end_url = settings.FRONTEND_BASE_URL + '/signup/'+quote(str(message))
            return redirect(front_end_url)
        
        message = 'Please check the link and try again'
        front_end_url = settings.FRONTEND_BASE_URL + '/signup/'+quote(str(message))
        return redirect(front_end_url)


class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response({'token': serializer.data.get('token')}, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(
            {
                'username': serializer.data.get('username'),
                'email': serializer.data.get('email')
            }, status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class RequestPasswordResetAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        """
        When a user posts an email here.
        It's validated and a 'password reset email' is sent
        to their registered email
        """
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.data.get('email',None)
        reset_manager = PasswordResetManager(request)
        reset_manager.request_password_reset(user_email)
        return Response({'message':'Email sent. Please check your inbox for a password reset email.'}, status = status.HTTP_200_OK)
       

class ResetPasswordAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = PasswordResetSerializer

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token',None)
        reset_manager = PasswordResetManager(request)

        user = reset_manager.get_user_from_token(token)
        if user is not None:
            front_url = settings.FRONTEND_BASE_URL + '/password-reset/' + token
            return redirect(front_url)
        else:
            front_url = settings.FRONTEND_BASE_URL + '/password-reset/invalid-token'
            return redirect(front_url)    

    def put(self, request,token):

        serializer_data = request.data.get('user',{})

        reset_manager = PasswordResetManager(request)
        user = reset_manager.get_user_from_token(token) 
        
        serializer = self.serializer_class(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data.get('password'))
        user.save()
        return Response({"password-reset":"Your password has been updated"}, status=status.HTTP_200_OK)
        

class FacebookLoginAPIview(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FacebookSocialAuthSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):

        auth_token = request.data.get('auth_token', {})

        serializer = self.serializer_class(data={'auth_token': auth_token})
        serializer.is_valid(raise_exception=True)
        social_user = FacebookSocialAuthSerializer.check_facebook_auth_token(self, auth_token)
        serializer=UserSerializer(social_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class GoogleLoginAPIview(GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = GoogleSocialAuthSerializer
    
    def post(self, request):

        auth_token = request.data.get('auth_token', {})

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        social_user = GoogleSocialAuthSerializer.check_google_auth_token(self, auth_token)
        serializer = UserSerializer(social_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class TwitterLoginAPIview(GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = TwitterSocialAuthSerializer

    def post(self, request):

        access_token = request.data.get('access_token', {})
        access_token_secret = request.data.get('access_token_secret', {})

        serializer = self.serializer_class(data={'access_token': access_token, 
                                                 'access_token_secret': access_token_secret})
        serializer.is_valid(raise_exception=True)
        social_user = TwitterSocialAuthSerializer.checking_auth_tokens(self, access_token, access_token_secret)
        serializer=UserSerializer(social_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
