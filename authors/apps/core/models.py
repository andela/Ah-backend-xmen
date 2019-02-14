from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from authors.apps.authentication.models import User,UserManager
from rest_framework import serializers
from django.conf import settings
from django.urls import reverse
import jwt
import datetime
from authors.apps.notifications.utils import permissions
import urllib.parse

class PasswordResetManager:
    """
    This handles password reset requests
    password reset link verifications and
    updating the user model with the new password
    """

    def __init__(self,request):
        """prepare up email params"""
        self.sender_email = 'authors.haven.5@gmail.com'
        self.token_generator = PasswordResetTokenGenerator()
        self.subject = "Reset your Password"
        self.account_recovery_endpoint = request.build_absolute_uri('/api/users/password-reset/')

    def request_password_reset(self,email):
        """Handles request to reset email"""
        user = self.find_user_by_email(email)

        if user is None:
            raise serializers.ValidationError("User with that email does not exist.")

        self.receiver_email = user.email

        #generate user token to be used in password reset link
        token = jwt.encode({'email': user.email,
                             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                             },
                            settings.SECRET_KEY
                            ,algorithm='HS256')

        #render password reset email from template
        context = {
            'username' : user.username,
            'action_url' : self.account_recovery_endpoint+token.decode('ascii')
        }
        rendered_string =  render_to_string('password_reset_email.txt', context)


   #send password reset email to user
        return (self.send(rendered_string),token.decode('ascii'))

    def get_user_from_token(self,token):
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithm='HS256')
            return self.find_user_by_email(payload['email'])
        except :
            return None

    def find_user_by_email(self,email):
        email = UserManager.normalize_email(email)
        try:
            user =  User.objects.get(email=email)
            return user
        except:
            return None

    def send(self,email_text):
        """Sends email_text to recipient"""
        return send_mail(
            self.subject,
            email_text,
            self.sender_email,
            [self.receiver_email],
            fail_silently=False
      )


class EmailNotificationDispatch:
    def __init__(self):
        self.sender_email = 'authors.haven.5@gmail.com'
        self.subject = "AH - You Have a new notificaton"

    def make_token(self, email, permission_type):
        return jwt.encode({'email': email,
                            'permission_type':permission_type,
                             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
                             },
                            settings.SECRET_KEY
                            ,algorithm='HS256').decode('ascii')

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
            return payload['email'], payload['permission_type']
        except Exception as e:
            raise serializers.ValidationError(str(e))
        
    def build_and_send(self, request, notification, notification_permission):
        self.receiver_email = notification.receiver.user.email
        opt_out_url = settings.FRONTEND_BASE_URL + \
                        reverse('notifications:perms', \
                            kwargs={'permission_type': \
                                    self.make_token(self.receiver_email, \
                                    notification_permission)})[4:]

        opt_out_all_url =  settings.FRONTEND_BASE_URL + \
                            reverse('notifications:perms',\
                                kwargs={'permission_type': 
                                self.make_token(self.receiver_email, \
                                permissions.RECEIVE_NOTIFICATION_EMAILS)})[4:]

        notification.action_link = settings.FRONTEND_BASE_URL + \
                            urllib.parse.urlparse(
                                notification.action_link).path[4:]
        context = {
            'username': notification.receiver.user.username,
            'notification_message' : notification.__str__(),
            'notification_action_url' : notification.action_link,
            'notification_opt_out_url': opt_out_url,
            'notification_opt_out_all_url': opt_out_all_url
        }
        self.message = render_to_string('notification_email.txt', context) 
        self.send()

    def send(self):
        """Sends email_text to recipient"""
        return send_mail(
            self.subject,
            self.message,
            self.sender_email,
            [self.receiver_email],
            fail_silently=True
        )


email_dispatch = EmailNotificationDispatch()
