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


def check_if_is_author(article, request_obj):
        if str(article.author) != str(request_obj.user.username):
            raise PermissionDenied(
                error_messages['permission_denied']
            )
        return False
