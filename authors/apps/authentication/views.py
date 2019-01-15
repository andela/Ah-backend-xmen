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
    PasswordResetRequestSerializer, PasswordResetSerializer
)


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
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

class RequestPasswordResetAPIView(APIView):
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
       

class ResetPasswordAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = PasswordResetSerializer

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token',None)
        reset_manager = PasswordResetManager(request)

        user = reset_manager.get_user_from_token(token)
        if user is not None:
            return Response({"token":"token is Valid, replace with 'set new password' form."}, status=status.HTTP_200_OK)
        else:
            return Response({"token":"token is not valid"}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request,token):

        serializer_data = request.data.get('user',{})

        reset_manager = PasswordResetManager(request)
        user = reset_manager.get_user_from_token(token) 
        
        serializer = self.serializer_class(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data.get('password'))
        user.save()
        return Response({"password-reset":"Your password has been updated"} , status=status.HTTP_200_OK)
        