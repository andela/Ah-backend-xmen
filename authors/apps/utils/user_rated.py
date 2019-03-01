from authors.apps.articles.models import (
	ArticleRating)
	


def get_user_rated(self,obj):
    count = ArticleRating.objects.filter(
    article_id=obj.pk, user=self.context['request'].user.pk).count()
    return count==1