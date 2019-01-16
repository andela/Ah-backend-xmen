import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User

"""Configure JWT Here"""


class JWTAuthentication(authentication.BaseAuthentication):
    """This class handles authentication of the JSON Web Tokens provided by the user"""

    def authenticate(self, request):
        """This method checks the Authorization header of every request

        Args:
            request (Request object): Django Request context

        Returns:
            None: Failed Authentication
            (user, token): On Successful Authentication.
        """
        # The 'auth_header' is an array with two elements:
        #
        #       1) The name of the authentication header (In this case 'Token'),
        #       2) The JWT to be authenticated against
        #
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            return None

        if len(auth_header) != 2:
            msg = 'Invalid Token'
            raise exceptions.AuthenticationFailed(msg)

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix != 'Bearer':
            msg = 'Use a Bearer Token'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(request, token)

    def authenticate_credentials(self, request, token):
        """This method authenticates the given credentials

        Args:
            request (Request object): Django Request context
            token (str): JSON Web Token

        Returns:
            None: Failed Authentication
            (user, token): Successful Authentication.
        """
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
        except jwt.InvalidTokenError:
            msg = 'Invalid token. Could not decode token'
            raise exceptions.AuthenticationFailed(msg)

        except jwt.ExpiredSignatureError:
            msg = 'Token expired, please login again.'
            raise exceptions.AuthenticationFailed(msg)
        token_data = payload['user_data'].split()

        try:
            token_data = payload['user_data'].split()
            user = User.objects.get(
                email=token_data[0], username=token_data[1])
        except User.DoesNotExist:
            msg = 'No user matching this token'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = "User has been deactivated"
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)
