from authors.apps.utils.renderers import AppJSONRenderer


class CommentJSONRenderer(AppJSONRenderer):
    name = 'comments'


class ReplyJSONRenderer(AppJSONRenderer):
    name = 'comment_replies'
