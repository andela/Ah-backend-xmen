
from django.urls import reverse
from .test_base_class import BaseTestClass
import jwt
import datetime
from authors import settings


class TestModel(BaseTestClass):
    def _make_request(self, method_, url):
        if method_ == 'put':
            return self.client.put(
                url,
                content_type='application/json', 
                HTTP_AUTHORIZATION='Bearer ' + self.test_user_token
            )
        elif method_ == 'get':
            return self.client.get(
                url,
                content_type='application/json', 
                HTTP_AUTHORIZATION='Bearer ' + self.test_user_token
            )

    def test_get_notifications_empty_succeeds(self):
        response = self._make_request(
            'get', reverse('notifications:task', kwargs={'task': 'all'}))
        self.assertEqual(0, len(response.data))

    def test_get_notifications_not_empty_succeeds(self):
        self.add_demo_notifications()
        response = self._make_request(
            'get',reverse('notifications:task', kwargs={'task': 'unread'}))
        self.assertEqual(2, len(response.data))

    def test_get_notifications_invalid_task_fails(self):
        response = self._make_request(
            'get',reverse('notifications:task', kwargs={'task': 'invalid_task'}))
        self.assertEqual(400, response.status_code)

    def test_mark_all_as_read_succeeds(self):
        self.add_demo_notifications()    
        response = self._make_request(
            'put', reverse('notifications:task', kwargs={'task': 'all'}))
        response = self._make_request(
            'get', reverse('notifications:task', kwargs={'task': 'unread'}))
        self.assertEqual(0, len(response.data))

    def test_mark_all_as_read_fails(self):
        self.add_demo_notifications()    
        response = self._make_request(
            'put', reverse('notifications:task', kwargs={'task': 'allls'}))
        self.assertEqual(400, response.status_code)

    def test_optout_succeeds(self):
        token = jwt.encode(
            {'email': self.test_user.email,
             'permission_type': 'PROFILE_FOLLOW',
             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
             }, settings.SECRET_KEY, algorithm='HS256').decode('ascii')
        response = self._make_request(
         'get', reverse(
             'notifications:perms', kwargs={'permission_type': token}))
        self.assertEqual(200, response.status_code)

    def test_optout_twice_fails_succeeds(self):
        token = jwt.encode(
            {'email': self.test_user.email,
             'permission_type': 'PROFILE_FOLLOW',
             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
             }, settings.SECRET_KEY, algorithm='HS256').decode('ascii')

        response = self._make_request(
            'get', reverse(
                'notifications:perms', kwargs={'permission_type': token}))
        self.assertEqual(200, response.status_code)
        response = self._make_request(
            'get', reverse(
                'notifications:perms', kwargs={'permission_type': token}))
        self.assertIn(
            'You already opted out', response.data.get('permissions'))

    def test_remove_permission_invalid_permission_fails(self):
        response = self._make_request(
            'put', reverse('notifications:perms', 
                           kwargs={'permission_type': 'BAD_TYPE'}))
        self.assertEqual(400, response.status_code)
        self.assertIn(
            'notification type is unknown', response.data.get('errors')[0])

    def test_toggle_opt_into_email_notifications_succeeds(self):
        token = jwt.encode(
            {'email': self.test_user.email,
             'permission_type': 'RECEIVE_NOTIFICATION_EMAILS',
             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
             }, settings.SECRET_KEY, algorithm='HS256').decode('ascii')
        response = self._make_request(
            'get', reverse('notifications:perms', 
                           kwargs={'permission_type': token}))
        response = self._make_request(
            'put', reverse(
                'notifications:perms', 
                kwargs={'permission_type': 'RECEIVE_NOTIFICATION_EMAILS'}))
        self.assertEqual(200, response.status_code)
        self.assertIn(
            'notification opt in is successful',
            response.data.get('permissions'))

    def test_toggle_opt_into_email_notifications_twice_fails_succeeds(self):
        token = jwt.encode(
            {'email': self.test_user.email,
             'permission_type': 'RECEIVE_NOTIFICATION_EMAILS',
             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
             }, settings.SECRET_KEY, algorithm='HS256').decode('ascii')

        response = self._make_request(
            'get', reverse('notifications:perms',
                           kwargs={'permission_type': token}))
        response = self._make_request(
            'put', reverse('notifications:perms', 
                           kwargs={'permission_type':
                                   'RECEIVE_NOTIFICATION_EMAILS'}))

        self.assertEqual(200, response.status_code)
        self.assertIn(
            'notification opt in is successful',
            response.data.get('permissions'))
        response = self._make_request(
            'put', reverse('notifications:perms',
                           kwargs={'permission_type': 
                                   'RECEIVE_NOTIFICATION_EMAILS'}))
        self.assertEqual(200, response.status_code)
        self.assertIn(
            'You already opted into this notification', 
            response.data.get('permissions'))

    def test_toggle_invalid_jwt_notification_opt_out_fails(self):
        token = jwt.encode(
            {'email': self.test_user.email,
             'permission_type': 'RECEIVE_NOTIFICATION_EMAILS',
             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
             }, settings.SECRET_KEY, algorithm='HS256').decode('ascii')+'qq'
        response = self._make_request(
            'get', reverse('notifications:perms',
                           kwargs={'permission_type': token}))
        self.assertEqual(400, response.status_code)
