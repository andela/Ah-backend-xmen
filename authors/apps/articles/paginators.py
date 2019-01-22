from rest_framework.pagination import LimitOffsetPagination


class ArticleLimitOffSetPagination(LimitOffsetPagination):
    default_limit = 10
    offset_query_param = 'page'
