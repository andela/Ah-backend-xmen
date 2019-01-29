from rest_framework.exceptions import PermissionDenied
from authors.apps.utils.messages import error_messages


def if_owner_permission(request_obj, **kwargs):
    """Checks if user owns a resource

    Args:
    request_obj (Django request):

    kwargs (dict): The mandatory key-value pairs are:
        username (str): The username from the profile to be edited

    raises:
         PermissionDenied:
         - if user is not the owner of the profile

    """
    if kwargs.get("username") != request_obj.user.username:
        raise PermissionDenied(
            error_messages.get('permission_denied'))


def check_if_is_author(instance, request_obj):
        if str(instance.author) != str(request_obj.user.username):
            raise PermissionDenied(
                error_messages['permission_denied']
            )
        return False


def can_report(article, request_object):
    if article.author == request_object.user.profile:
        raise PermissionDenied(
            error_messages.get('permission_denied')
        )
    return False


def check_if_can_track_history(instance_1, instance_2, request_object):
    if str(instance_1.author) != str(request_object.user.username) and str(instance_2.author) != str(request_object.user.username):
        raise PermissionDenied(
                error_messages['permission_denied']
            )
