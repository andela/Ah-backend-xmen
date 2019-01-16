from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    RequestPasswordResetAPIView,ResetPasswordAPIView,
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='user'),
    path('users/', RegistrationAPIView.as_view(), name='signup'),
    path('users/login/', LoginAPIView.as_view(), name='login'), 
    path('users/password-reset/', RequestPasswordResetAPIView.as_view(), name='request-password-reset'),
    path('users/password-reset/<token>/', ResetPasswordAPIView.as_view(), name='password-reset'),
]
