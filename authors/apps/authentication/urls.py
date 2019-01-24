from django.urls import path
from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    EmailVerificationAPIView, RequestPasswordResetAPIView, ResetPasswordAPIView,
    FacebookLoginAPIview, GoogleLoginAPIview, TwitterLoginAPIview
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='user'),
    path('user/<pk>/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view(), name='signup'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('users/password-reset/', RequestPasswordResetAPIView.as_view(),
         name='request-password-reset'),
    path('users/password-reset/<token>/',
         ResetPasswordAPIView.as_view(), name='password-reset'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('users/registration-confirmation/<uuid>/<token>/',
         EmailVerificationAPIView.as_view(), name='email-verification'),
    path('users/facebook-login/', FacebookLoginAPIview.as_view(), name='facebook'),
    path('users/google-login/', GoogleLoginAPIview.as_view(), name='google'),
    path('users/twitter-login/', TwitterLoginAPIview.as_view(), name='twitter'),
]
