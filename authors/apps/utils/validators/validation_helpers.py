import re

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from authors.apps.articles.models import Article
from authors.apps.authentication.models import User


def validate_password(password):
    if password is None:
        raise serializers.ValidationError("A new password is required to request reset password.")
    elif len(password)<8:
       raise serializers.ValidationError("Password must be longer than 8 characters.")
    elif re.search(r'(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])', password) is None:
        raise serializers.ValidationError("Password should at least contain a number, capital and small letter.")
    return password

def validate_username(username):
    check_username = User.objects.filter(username=username)
    if check_username.exists():
        raise serializers.ValidationError("Username already exists.")
    username_first_char = username[:1]
    if re.search(r'[\W\t\s\d]', username_first_char):
        raise serializers.ValidationError("Username must start with a letter.")
    if re.search(r'[\W\t\s]', username):
        raise serializers.ValidationError("Username cannot contain special characters.")
    if len(username.strip()) < 5:
        raise serializers.ValidationError("Username must be longer than 5 characters.")
    return username

def validate_index(index, slug):
    article = get_object_or_404(Article, slug=slug)
    article_length = len(article.body)
    if index is None:
        return
    if int(index) > article_length:
        raise serializers.ValidationError("Index must not exceed article length.")
    return index
