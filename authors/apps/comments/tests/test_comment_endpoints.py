from authors.apps.authentication.tests_ import test_base_class
from django.shortcuts import reverse
import json
class TestCommentEndpoints(test_base_class.BaseTestClass):
    def test_create_comment_on_article_successed(self):
        """
        Tests successful commenting on an article
        Returns:
            201 status code if a comment is added to an article
        """
        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comments',args=[self.slug]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(self.comment_data))
        self.assertEqual(resp.status_code,201)
    
    def test_get_all_comments_of_an_article_successed(self):
        """
        Tests getting all comments that belong to an article
        Returns:
            if all comments are returned a 200 status code is returned
        """
        self.slug=self.created_article.slug
        resp=self.client.get(reverse('comments:comments',args=[self.slug]),HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token)
        self.assertEqual(resp.status_code,200)
    def test_get_a_single_comment_of_an_article_successed(self):
        """
        test get a one comment for an article
        Returns:
            201 status code if a comment is added to an article
        """

        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comments',args=[self.slug]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(self.comment_data))
        self.slug=self.created_article.slug
        self.article_id=resp.data['comment']['id']
        print(self.article_id)
        resp=self.client.get(reverse('comments:comment-detail',args=[self.slug,self.article_id]),
        content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token)
        self.assertEqual(resp.status_code,200)
    
    def test_update_a_comment_of_an_article_successed(self):
        """
        test update a comment for an article
        Returns:
            201 status code if a comment  is updated to by author of the comment
        """

        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comments',args=[self.slug]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(self.comment_data))
        self.slug=self.created_article.slug
        self.article_id=resp.data['comment']['id']
        print(self.article_id)
        resp=self.client.put(reverse('comments:comment-detail',args=[self.slug,self.article_id]),
        content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(self.comment_update))
        self.assertEqual(resp.status_code,201)
    
    
    def test_update_a_comment_of_an_article_fails_if_not_author(self):
        """
        test update a comment for an article fails if user is not author of the comment
        Returns:
            403 is returned if a person who did write the comment tries to update it
        """

        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comments',args=[self.slug]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(self.comment_data))
        self.slug=self.created_article.slug
        self.article_id=resp.data['comment']['id']
        print(self.article_id)
        resp=self.client.put(reverse('comments:comment-detail',args=[self.slug,self.article_id]),
        content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.not_author_token,data=json.dumps(self.comment_update))
        self.assertEqual(resp.status_code,403)
    
    def test_delete_a_comment_of_an_article_fails_if_not_author_(self):
        """
        tests failing deleting of a comment that a user didnot write
        Returns:
            403 is returned if a person who did write the comment tries to delete it
        """

        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comments',args=[self.slug]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(self.comment_data))
        self.slug=self.created_article.slug
        self.article_id=resp.data['comment']['id']
        print(self.article_id)
        resp=self.client.delete(reverse('comments:comment-detail',args=[self.slug,self.article_id]),
        content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.not_author_token,data=json.dumps(self.comment_update))
        self.assertEqual(resp.status_code,403)
    
    def test_delete_a_comment_of_an_article_successed(self):
        """
        testing deleting of a comment if the user is the author of the comment
        Returns:
            200 status code is commented is succesfully deleted
        """

        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comments',args=[self.slug]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(self.comment_data))
        self.slug=self.created_article.slug
        self.article_id=resp.data['comment']['id']
        print(self.article_id)
        resp=self.client.delete(reverse('comments:comment-detail',args=[self.slug,self.article_id]),
        content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(self.comment_update))
        self.assertEqual(resp.status_code,200)