from django_filters import FilterSet
from django_filters import rest_framework as filters
from .models import Article


class ArticleFilter(FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    author = filters.CharFilter('author__user__username',
                                lookup_expr='icontains')
    favorited = filters.CharFilter(field_name='favorited',
                                   lookup_expr='icontains',
                                   method='favorites_filter')
    tags = filters.CharFilter('tags', method='filter_by_tags')

    class Meta:
        model = Article
        fields = ('title', 'author', 'favorited', 'tags')

    def filter_by_tags(self, queryset, name, value):
        return queryset.filter(tags__icontains=value)

    def favorites_filter(self, qs, name, value):
        """
        favorites filter is based on the Article manager model
        """
        value = value.capitalize()
        return qs.filter(favorited=value).distinct()
