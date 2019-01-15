import random
import string
from django.utils.text import slugify


def unique_code_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def generate_slug(instance):
    return slugify(instance.title)
