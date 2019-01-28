from authors.apps.comments.models import Comment, CommentReply, CommentLike, CommentReplyLike
from authors.apps.authentication.tests_ import test_base_class
from authors.apps.comments.apps import CommentsConfig


class TestCommentModel(test_base_class.BaseTestClass):

    def test_comment_str_return_method(self):
        self.comment = Comment.objects.create(
            body='A comment body', author=self.profile, article=self.created_article)
        self.assertEqual(self.comment.__str__(), 'A comment body')

    def test_comment_reply_str__method(self):
        self.commentReply = CommentReply.objects.create(
            reply_body="A reply body", author=self.profile, comment=self.testcomment)
        self.assertEqual(self.commentReply.__str__(), 'A reply body')

    def test_comment_like_str_method(self):
        self.commentLike = CommentLike.objects.create(
            liked_by=self.profile, comment=self.testcomment, like_status=True)
        self.assertEqual('like by  testuser1', self.commentLike.__str__())

    def test_comment_reply_like_str_method(self):
        self.commentReplyLike = CommentReplyLike.objects.create(
            liked=True, reply_like_by=self.profile, comment_reply=self.testCommentReply)
        self.assertEqual(self.commentReplyLike.__str__(),
                         'reply liked by testuser1')


def test_comments_app_instance(self):
    self.assertEqual(CommentsConfig.name, 'comments')
