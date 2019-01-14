from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from authors.apps.authentication.models import User,UserManager
from rest_framework import serializers
from django.conf import settings
import jwt
import datetime

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

    def update_password(self,user,new_password):
        user.set_password(new_password)
        user.save()

    def send(self,email_text):
        """Sends email_text to recipient"""
        return send_mail(
            self.subject,
            email_text,
            self.sender_email,
            [self.receiver_email],
            fail_silently=False
      )
