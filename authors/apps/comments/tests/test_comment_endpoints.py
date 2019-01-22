from authors.apps.authentication.tests_ import test_base_class
from django.shortcuts import reverse
import json
from authors.apps.authentication.tests_ import test_data

class TestCommentEndpoints(test_base_class.BaseTestClass):
    def test_create_comment_on_article_succeeds(self):
        """
        Tests successful commenting on an article
        Returns:
            201 status code if a comment is added to an article
        """
        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comments',args=[self.slug]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(test_data.comment_data['comment_data']))
        self.assertEqual(resp.status_code,201)
    
    def test_get_all_comments_of_an_article_succeeds(self):
        """
        Tests getting all comments that belong to an article
        Returns:
            if all comments are returned a 200 status code is returned
        """
        self.slug=self.created_article.slug
        resp=self.client.get(reverse('comments:comments',args=[self.slug]),HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token)
        self.assertEqual(resp.status_code,200)
    def test_get_a_single_comment_of_an_article_succeeds(self):
        """
        test get a one comment for an article
        Returns:
            201 status code if a comment is added to an article
        """

        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comments',args=[self.slug]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id=resp.data['comment']['id']
        resp=self.client.get(reverse('comments:comment-detail',args=[self.slug,self.comment_id]),
        content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token)
        self.assertEqual(resp.status_code,200)
    
    def test_update_a_comment_of_an_article_succeeds(self):
        """
        test update a comment for an article
        Returns:
            201 status code if a comment  is updated to by author of the comment
        """

        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comments',args=[self.slug]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id=resp.data['comment']['id']
        resp=self.client.put(reverse('comments:comment-detail',args=[self.slug,self.comment_id]),
        content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(test_data.comment_data['comment_update']))
        self.assertEqual(resp.status_code,201)
    
    
    def test_update_a_comment_of_an_article_fails_if_not_author(self):
        """
        test update a comment for an article fails if user is not author of the comment
        Returns:
            403 is returned if a person who did write the comment tries to update it
        """

        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comments',args=[self.slug]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id=resp.data['comment']['id']
        resp=self.client.put(reverse('comments:comment-detail',args=[self.slug,self.comment_id]),
        content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.not_author_token,data=json.dumps(test_data.comment_data['comment_update']))
        self.assertEqual(resp.status_code,403)
    
    def test_delete_a_comment_of_an_article_fails_if_not_author_(self):
        """
        tests failing deleting of a comment that a user didnot write
        Returns:
            403 is returned if a person who did write the comment tries to delete it
        """

        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comments',args=[self.slug]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id=resp.data['comment']['id']
        resp=self.client.delete(reverse('comments:comment-detail',args=[self.slug,self.comment_id]),
        content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.not_author_token,data=json.dumps(test_data.comment_data['comment_update']))
        self.assertEqual(resp.status_code,403)
    
    def test_delete_a_comment_of_an_article_succeeds(self):
        """
        test deleting of a comment if the user is the author of the comment
        Returns:
            200 status code is commented is succesfully deleted
        """

        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comments',args=[self.slug]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id=resp.data['comment']['id']

        resp=self.client.delete(reverse('comments:comment-detail',args=[self.slug,self.comment_id]),
        content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(test_data.comment_data['comment_update']))
        self.assertEqual(resp.status_code,200)
        
    
    def test_create_a_reply_on_a_comment_succeeds(self):
        """
        test creating of a reply to a specific comment
        Returns:
            200 status code is commented is succesfully deleted
        """
        self.comment_id=self.testcomment.pk
        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comment-reply',args=[self.slug,self.comment_id]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(test_data.commentReply_data['reply_data']))
        self.assertEqual(resp.status_code,201)

    def test_get_all_comment_replies_succeeds(self):
        """
        test creating of a reply to a specific comment
        Returns:
            200 status code is commented is succesfully deleted
        """
        self.comment_id=self.testcomment.pk
        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comment-reply',args=[self.slug,self.comment_id]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(test_data.commentReply_data['reply_data']))
        resp_get_replies=self.client.get(reverse('comments:comment-reply',args=[self.slug,self.comment_id]),                                    HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        self.assertEqual(resp_get_replies.status_code,200)
    
    def test_get_detail_of_a_single_reply_succeeds(self):
        """
        tests gettting detail of a specific reply on a comment
        Returns:
            200 status code for True and 404 if false
        """
        self.comment_id=self.testcomment.pk
        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comment-reply',args=[self.slug,self.comment_id]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,data=json.dumps(test_data.commentReply_data['reply_data']))
        self.reply_id=resp.data['reply']['id']

        resp_get_reply_details=self.client.get(reverse('comments:comment-reply-detail',args=[self.slug,self.comment_id,self.reply_id]),HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token)
        self.assertEqual(resp_get_reply_details.status_code,200)
    
    def test_update_detail_of_a_single_reply_succeeds(self):
        """
        tests gettting detail of a specific reply on a comment
        Returns:
            200 status code for True and 404 if false
        """
        self.comment_id=self.testcomment.pk
        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comment-reply',args=[self.slug,self.comment_id]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' + self.test_user_token,data=json.dumps(test_data.commentReply_data['reply_data']))
        self.reply_id=resp.data['reply']['id']
        resp_update_reply_details=self.client.put(reverse('comments:comment-reply-detail',args=[self.slug,self.comment_id,self.reply_id]),HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,content_type='application/json',data=json.dumps(
                                   test_data.commentReply_data['reply_update_data']))
        self.assertEqual(resp_update_reply_details.status_code,201)

    def test_delete_detail_of_a_single_reply_succeeds(self):
        """
        tests gettting detail of a specific reply on a comment
        Returns:
            200 status code for True and 404 if false
        """
        self.comment_id=self.testcomment.pk
        self.slug=self.created_article.slug
        resp=self.client.post(reverse('comments:comment-reply',args=[self.slug,self.comment_id]),content_type='application/json',HTTP_AUTHORIZATION='Bearer ' + self.test_user_token,data=json.dumps(test_data.commentReply_data['reply_data']))
        self.reply_id=resp.data['reply']['id']
        resp_update_reply_details=self.client.delete(reverse('comments:comment-reply-detail',args=[self.slug,self.comment_id,self.reply_id]),HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token,content_type='application/json',data=json.dumps(
                                   test_data.commentReply_data['reply_update_data']))
        self.assertEqual(resp_update_reply_details.status_code,200)