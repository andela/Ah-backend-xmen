from authors.apps.comments.models import Comment
from authors.apps.authentication.tests_ import test_base_class
from authors.apps.comments.apps import CommentsConfig

class TestCommentModel(test_base_class.BaseTestClass):
    def test_comment_str_return_method(self):
        self.comment=Comment.objects.create(body='A comment body',author=self.profile,article=self.created_article)
        self.assertEqual(self.comment.__str__(),'A comment body')



def test_comments_app_instance(self):    
    self.assertEqual(CommentsConfig.name,'comments')

        

