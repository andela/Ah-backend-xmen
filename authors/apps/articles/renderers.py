
from authors.apps.utils.renderers import AppJSONRenderer

class ArticleJSONRenderer(AppJSONRenderer):
    name = 'articles'

class BookmarkJSONRenderer(AppJSONRenderer):
    name = 'bookmarks'
