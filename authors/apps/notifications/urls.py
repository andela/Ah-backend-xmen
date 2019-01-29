from django.urls import path

from .views import (
    NotiificationsAPIView,
    NotiificationsOptOutAPIView
)

urlpatterns = [
    path('<task>', NotiificationsAPIView.as_view(),  name='task'),
    path('perm/<permission_type>', NotiificationsOptOutAPIView.as_view(),
         name='perms')
]
