from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from authors.apps.utils.custom_permissions.permissions import check_if_is_author

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
