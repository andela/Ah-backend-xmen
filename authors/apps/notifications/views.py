from rest_framework import status, serializers
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Notification
from authors.apps.profiles.models import Profile
from .renderers import NotificationJSONRenderer
from .serializers import (
    NotificationSerializer
)
from .utils import permissions
from authors.apps.core.models import email_dispatch
from authors.apps.utils.messages import tasks


class NotiificationsAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (NotificationJSONRenderer,)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user.profile
        task = self.kwargs.get('task')
        if task.lower() == tasks['all']:
            return user.received_notifications.all()

        elif task.lower() == tasks['unread']:
            return user.received_notifications.filter(is_read=False)
        else:
            raise serializers.ValidationError(
                'task to be completed not understood. try "all"'
                )

    def put(self, request, task):
        user = Profile.objects.get(user=request.user)
        if task.lower() == tasks['all']:
            Notification.objects.mark_all_as_read(user)
            return Response({'message': 'all notifications marked as read.'},
                            status=status.HTTP_200_OK)
        else:
            raise serializers.ValidationError(
                'task to be completed not understood. try "all"'
                )


class NotiificationsOptOutAPIView(GenericAPIView):
    permission_classes = (AllowAny, IsAuthenticated,)
    renderer_classes = (NotificationJSONRenderer,)
    serializer_class = NotificationSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny, ] if self.request.method == 'GET'\
         else [IsAuthenticated, ]

        return super(NotiificationsOptOutAPIView, self).get_permissions()

    def get(self, request, permission_type):
        email, permission_type = email_dispatch.decode_token(permission_type)
        profile = get_object_or_404(Profile, user__email=email)
        if permission_type in profile.notification_perms:
            profile.notification_perms.remove(permission_type)
            profile.save()
            return Response(
                {'permissions': 
                 'Your notification opt out for {} is successful.'.format(
                    permission_type)},
                status=status.HTTP_200_OK)
        return Response({'permissions': 'You already opted out.'},
                        status=status.HTTP_200_OK)
   
    def put(self, request, permission_type):
        me = Profile.objects.get(user=request.user)
        permission_type = permission_type.strip().upper()
        if permission_type not in permissions.get_all():
            raise serializers.ValidationError(
                'This notification type is unknown.')
        if permission_type in me.notification_perms:
            return Response(
                            {'permissions':
                             'You already opted into this notification'},
                            status=status.HTTP_200_OK)
        me.notification_perms.append(permission_type)
        me.save()
        return Response(
                        {'permissions':
                         'Your notification opt in is successful.'},
                        status=status.HTTP_200_OK)
