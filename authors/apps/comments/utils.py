from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from authors.apps.utils.custom_permissions.permissions import check_if_is_author
from .models import Comment

def update_obj(request,id,Instance,serializer_class):
    """
    this function handles updating of a model 
    Args:
        request: a request object
        id[integer]:id of the object to be updated
        Instance[Class]:Class instance of the model to which the object belongs to
        serializer_class[A restframework serializer]:serializer class of the current view
    Returns:
        201 code if successful else False if updating fails
    """
    obj=get_object_or_404(Instance,pk=id)
    check_if_is_author(obj,request)
    serializer=serializer_class(obj,data=request.data,partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({
        'data':serializer.data
    },status=status.HTTP_201_CREATED)


def get_edit_history(obj):
    edit_history = []
    for item in list(obj.filter(history_type="~")):
        """ Assign signs to words """
        if item.history_type == "~":
            item.history_type = "update"

        """  edited item """
        edit_history_item = {
            "change_date": str(item.history_date),
            "history_id": item.history_id,
            "history_change_type": item.history_type,
            "body": get_body_field_name(obj, item)
            }
        edit_history.append(edit_history_item)
    return edit_history


def get_body_field_name(obj, item):
    if item in Comment.comment_history.all():
        return item.body
    else:
        return item.reply_body
