from authors.apps.authentication.tests_.test_base_class import BaseTestClass
import json
from authors.apps.authentication.tests_ import test_data


class TestHighlightComment(BaseTestClass):

    def test_comment_on_forward_highlighted_text_in_article_succeeds(self):
        """
        Tests successful forward highlight of text in an article
        before posting a comment
        """
        self.slug = self.created_article.slug
        response = self.client.post(
            f'/api/articles/{self.slug}/comments/',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.test_user_token,
            data=json.dumps(test_data.highlighted_comment['forward_highlight'])
            )
        self.assertEqual(response.status_code, 201)

    def test_comment_on_reverse_highlighted_text_in_article_succeeds(self):
        """
        Tests successful reverse highlight of text in an article
        before posting a comment
        """
        self.slug = self.created_article.slug
        response = self.client.post(
            f'/api/articles/{self.slug}/comments/',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.test_user_token,
            data=json.dumps(test_data.highlighted_comment['reverse_highlight'])
            )
        self.assertEqual(response.status_code, 201)


    def test_comment_on_highlight_ending_index_exceeding_article_length_fails(self):
        """
        Tests invalid highlight of text with an index
        exceeding the article length
        """
        self.slug = self.created_article.slug
        response = self.client.post(
            f'/api/articles/{self.slug}/comments/',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + self.test_user_token,
            data=json.dumps(test_data.highlighted_comment['invalid_highlight'])
            )
        self.assertEqual(response.status_code, 400)
