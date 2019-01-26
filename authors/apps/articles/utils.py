import random
import string
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.db.models import Avg


def unique_code_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def generate_slug(instance):
    return slugify(instance.title)


def get_likes_or_dislkes(**kwargs):
    """
    Fetches the number of likes and dislikes

    args:
        Keyword arguments: These are include the model, id of an article and
                            the like status of the article

    Returns:
        filtered_likes(int): number of likes or dislikes of an article
    """
    likes = kwargs.get('model').objects.all().filter(
        like_article=kwargs.get('like_article')
    )
    filtered_likes = likes.filter(article_id=kwargs.get('article_id'))
    return filtered_likes.count()


def get_like_status(like_status, arg_1, arg_2):
    """
    Fetches a string for a particluar like_status

    args:
        like_status(boolean): It's either a True for a like
                                or False for a dislike
        arg_1(str)
        arg_2(str)

    Returns:
        arg_1(str): Incase the like_status is True
        arg_2(str): Incase the like_status is False
    """
    return arg_1 if like_status else arg_2


def get_usernames(**kwargs):
    """
    Fetches a list of usernames

    args:
        Keyword arguments: These are include the model, id of an article and
                            the like status of the article

    Returns:
        usernames(list): usernames of registered users
    """
    filtered_list = kwargs.get('model').objects.all().filter(
        article_id=kwargs.get('article_id')
    ).filter(like_article=kwargs.get('like_article'))
    usernames = []
    for likes in filtered_list:
        usernames.append(get_user_model().objects.get(
            pk=likes.user.id).username)
    return usernames


def get_average_value(**kwargs):
    avg_ratings = kwargs.get('model').objects.all().filter(
        article_id=kwargs.get('article_id')
    ).aggregate(Avg('rating')).get('rating__avg')
    if avg_ratings is None:
        return 0
    else:
        return int(avg_ratings)
