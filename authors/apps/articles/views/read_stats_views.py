from rest_framework import generics, serializers
from authors.apps.articles.serializers import ReadStatsSerializer
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from authors.apps.articles.models import Article, ReadStats
from rest_framework.response import Response
from rest_framework import status

from authors.apps.authentication.models import User


class ReadStatsAPIView(generics.GenericAPIView):
    """
    Class that enables the author or user to view their reading
    stats that is the number of times an article has been read
    """
    serializer_class = ReadStatsSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, username):
        """ this is to get the readstats """
        reader_stats = ReadStats.objects.filter(user=request.user.id)
        reader_statsCount=reader_stats.count()
        serializer=self.serializer_class(reader_stats, many=True)
        return Response({
            "stats":serializer.data,
            "count":reader_statsCount
        }, )
        