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
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comments', args=[self.slug]), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token, data=json.dumps(test_data.comment_data['comment_data']))
        self.assertEqual(resp.status_code, 201)

    def test_get_all_comments_of_an_article_succeeds(self):
        """
        Tests getting all comments that belong to an article
        Returns:
            if all comments are returned a 200 status code is returned
        """
        self.slug = self.created_article.slug
        resp = self.client.get(reverse('comments:comments', args=[self.slug]), HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token)
        self.assertEqual(resp.status_code, 200)

    def test_get_a_single_comment_of_an_article_succeeds(self):
        """
        test get a one comment for an article
        Returns:
            201 status code if a comment is added to an article
        """

        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comments', args=[self.slug]), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token, data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id = resp.data['comment']['id']
        resp = self.client.get(reverse('comments:comment-detail', args=[self.slug, self.comment_id]),
                               content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token)
        self.assertEqual(resp.status_code, 200)

    def test_update_a_comment_of_an_article_succeeds(self):
        """
        test update a comment for an article
        Returns:
            201 status code if a comment  is updated to by author of the comment
        """

        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comments', args=[self.slug]), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token, data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id = resp.data['comment']['id']
        resp = self.client.put(reverse('comments:comment-detail', args=[self.slug, self.comment_id]),
                               content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                               self.test_user_token, data=json.dumps(test_data.comment_data['comment_update']))
        self.assertEqual(resp.status_code, 201)

    def test_update_a_comment_of_an_article_fails_if_not_author(self):
        """
        test update a comment for an article fails if user is not author of the comment
        Returns:
            403 is returned if a person who did write the comment tries to update it
        """

        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comments', args=[self.slug]), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token, data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id = resp.data['comment']['id']
        resp = self.client.put(reverse('comments:comment-detail', args=[self.slug, self.comment_id]),
                               content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                               self.not_author_token, data=json.dumps(test_data.comment_data['comment_update']))
        self.assertEqual(resp.status_code, 403)

    def test_delete_a_comment_of_an_article_fails_if_not_author_(self):
        """
        tests failing deleting of a comment that a user didnot write
        Returns:
            403 is returned if a person who did write the comment tries to delete it
        """

        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comments', args=[self.slug]), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token, data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id = resp.data['comment']['id']
        resp = self.client.delete(reverse('comments:comment-detail', args=[self.slug, self.comment_id]),
                                  content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                  self.not_author_token, data=json.dumps(test_data.comment_data['comment_update']))
        self.assertEqual(resp.status_code, 403)

    def test_delete_a_comment_of_an_article_succeeds(self):
        """
        test deleting of a comment if the user is the author of the comment
        Returns:
            200 status code is commented is succesfully deleted
        """

        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comments', args=[self.slug]), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token, data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id = resp.data['comment']['id']

        resp = self.client.delete(reverse('comments:comment-detail', args=[self.slug, self.comment_id]),
                                  content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                  self.test_user_token, data=json.dumps(test_data.comment_data['comment_update']))
        self.assertEqual(resp.status_code, 200)

    def test_create_a_reply_on_a_comment_succeeds(self):
        """
        test creating of a reply to a specific comment
        Returns:
            200 status code is commented is succesfully deleted
        """
        self.comment_id = self.testcomment.pk
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comment-reply', args=[self.slug, self.comment_id]), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token, data=json.dumps(test_data.commentReply_data['reply_data']))
        self.assertEqual(resp.status_code, 201)

    def test_get_all_comment_replies_succeeds(self):
        """
        test creating of a reply to a specific comment
        Returns:
            200 status code is commented is succesfully deleted
        """
        self.comment_id = self.testcomment.pk
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comment-reply', args=[self.slug, self.comment_id]), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token, data=json.dumps(test_data.commentReply_data['reply_data']))
        resp_get_replies = self.client.get(reverse('comments:comment-reply', args=[
                                           self.slug, self.comment_id]),                                    HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        self.assertEqual(resp_get_replies.status_code, 200)

    def test_get_detail_of_a_single_reply_succeeds(self):
        """
        tests gettting detail of a specific reply on a comment
        Returns:
            200 status code for True and 404 if false
        """
        self.comment_id = self.testcomment.pk
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comment-reply', args=[self.slug, self.comment_id]), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token, data=json.dumps(test_data.commentReply_data['reply_data']))
        self.reply_id = resp.data['reply']['id']

        resp_get_reply_details = self.client.get(reverse('comments:comment-reply-detail', args=[self.slug, self.comment_id, self.reply_id]), HTTP_AUTHORIZATION='Bearer ' +
                                                 self.test_user_token)
        self.assertEqual(resp_get_reply_details.status_code, 200)

    def test_update_detail_of_a_single_reply_succeeds(self):
        """
        tests gettting detail of a specific reply on a comment
        Returns:
            200 status code for True and 404 if false
        """
        self.comment_id = self.testcomment.pk
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comment-reply', args=[self.slug, self.comment_id]), content_type='application/json',
                                HTTP_AUTHORIZATION='Bearer ' + self.test_user_token, data=json.dumps(test_data.commentReply_data['reply_data']))
        self.reply_id = resp.data['reply']['id']
        resp_update_reply_details = self.client.put(reverse('comments:comment-reply-detail', args=[self.slug, self.comment_id, self.reply_id]), HTTP_AUTHORIZATION='Bearer ' +
                                                    self.test_user_token, content_type='application/json', data=json.dumps(
            test_data.commentReply_data['reply_update_data']))
        self.assertEqual(resp_update_reply_details.status_code, 201)

    def test_delete_detail_of_a_single_reply_succeeds(self):
        """
        tests gettting detail of a specific reply on a comment
        Returns:
            200 status code for True and 404 if false
        """
        self.comment_id = self.testcomment.pk
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comment-reply', args=[self.slug, self.comment_id]), content_type='application/json',
                                HTTP_AUTHORIZATION='Bearer ' + self.test_user_token, data=json.dumps(test_data.commentReply_data['reply_data']))
        self.reply_id = resp.data['reply']['id']
        resp_update_reply_details = self.client.delete(reverse('comments:comment-reply-detail', args=[self.slug, self.comment_id, self.reply_id]), HTTP_AUTHORIZATION='Bearer ' +
                                                       self.test_user_token, content_type='application/json', data=json.dumps(
            test_data.commentReply_data['reply_update_data']))
        self.assertEqual(resp_update_reply_details.status_code, 200)

    def test_like_a_comment_succeeds(self):
        """
        tests liking a specific comment
        Returns:
            200 ok status code if comment is successfully liked
        """
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comments', args=[self.slug]), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token, data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id = resp.data['comment']['id']

        resp = self.client.put(reverse('comments:comment-like', args=[self.slug, self.comment_id]),
                               content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + self.test_user_token, data=json.dumps({}))

        self.assertEqual(resp.status_code, 200)

    def test_like_a_comment_that_you_already_liked_fails(self):
        """
        tests liking a comment you alreday liked 
        Returns:
            400 bad request status code if comment you already liked comment before
        """
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comments', args=[self.slug]), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token, data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id = resp.data['comment']['id']

        resp = self.client.put(reverse('comments:comment-like', args=[self.slug, self.comment_id]),
                               content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + self.test_user_token, data=json.dumps({}))

        resp = self.client.put(reverse('comments:comment-like', args=[self.slug, self.comment_id]),
                               content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + self.test_user_token, data=json.dumps({}))

        self.assertEqual(resp.status_code, 400)

    def test_remove_a_like_on_a_comment_succeeds(self):
        """
        tests liking a specific comment
        Returns:
            200 ok status code if comment like is succeccfully removed
        """
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comments', args=[self.slug]), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token, data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id = resp.data['comment']['id']

        resp = self.client.put(reverse('comments:comment-like', args=[self.slug, self.comment_id]),
                               content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + self.test_user_token, data=json.dumps({}))

        resp_remove_like = self.client.delete(reverse('comments:comment-like', args=[
                                              self.slug, self.comment_id]), HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)

        self.assertEqual(resp_remove_like.status_code, 200)

    def test_remove_a_like_on_a_comment_you_havenot_liked_fails(self):
        """
        tests liking a specific comment
        Returns:
            200 ok status code if comment like is succeccfully removed
        """
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comments', args=[self.slug]), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token, data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id = resp.data['comment']['id']

        resp_remove_like = self.client.delete(reverse('comments:comment-like', args=[
                                              self.slug, self.comment_id]), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)

        self.assertEqual(resp_remove_like.status_code, 400)

    def test_get_all_likes_on_a_comment_succeeds(self):
        """
        tests liking a specific comment
        Returns:
            200 ok status code if comment like is succeccfully removed
        """
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comments', args=[self.slug]), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
                                self.test_user_token, data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id = resp.data['comment']['id']

        resp = self.client.put(reverse('comments:comment-like', args=[self.slug, self.comment_id]),
                               content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + self.test_user_token, data=json.dumps({}))

        resp_get_likes = self.client.get(reverse('comments:comment-like', args=[
                                         self.slug, self.comment_id]), HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)

        self.assertEqual(resp_get_likes.status_code, 200)

    def test_like_a_comment_reply_succeeds(self):
        """
        Test like a specific comment reply
        Returns:
            200 ok status code if a reply is successfully liked
        """
        self.comment_id = self.testcomment.pk
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comment-reply', args=[self.slug, self.comment_id]), content_type='application/json',
                                HTTP_AUTHORIZATION='Bearer ' + self.test_user_token, data=json.dumps(test_data.commentReply_data['reply_data']))
        self.reply_id = resp.data['reply']['id']

        resp_like_comment_reply = self.client.put(reverse('comments:comment-reply-like', args=[self.slug, self.comment_id, self.reply_id]), content_type='application/json', data=json.dumps({}),
                                                  HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        self.assertEqual(resp_like_comment_reply.status_code, 201)

    def test_like_a_comment_reply_fails_if_already_liked_reply(self):
        """
        Test like a specific comment reply fails if user already liked the reply
        Returns:
             400 status code if a reply is was already liked
        """
        self.comment_id = self.testcomment.pk
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comment-reply', args=[self.slug, self.comment_id]), content_type='application/json',
                                HTTP_AUTHORIZATION='Bearer ' + self.test_user_token, data=json.dumps(test_data.commentReply_data['reply_data']))
        self.reply_id = resp.data['reply']['id']

        resp_like_comment_reply = self.client.put(reverse('comments:comment-reply-like', args=[self.slug, self.comment_id, self.reply_id]), content_type='application/json', data=json.dumps({}),
                                                  HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)

        resp_like_comment_reply_again = self.client.put(reverse('comments:comment-reply-like', args=[self.slug, self.comment_id, self.reply_id]), content_type='application/json', data=json.dumps({}),
                                                        HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)

        self.assertEqual(resp_like_comment_reply_again.status_code, 400)

    def test_get_all_reply_likes_succeeds(self):
        """
        Test get all likes a specific comment reply
        Returns:
             200 status code if all likes are returned 
        """
        self.comment_id = self.testcomment.pk
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comment-reply', args=[self.slug, self.comment_id]), content_type='application/json',
                                HTTP_AUTHORIZATION='Bearer ' + self.test_user_token, data=json.dumps(test_data.commentReply_data['reply_data']))
        self.reply_id = resp.data['reply']['id']

        resp_like_comment_reply = self.client.put(reverse('comments:comment-reply-like', args=[self.slug, self.comment_id, self.reply_id]), content_type='application/json', data=json.dumps({}),
                                                  HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)

        resp_get_all_comment_reply_likes = self.client.get(reverse('comments:comment-reply-like', args=[
                                                           self.slug, self.comment_id, self.reply_id]), HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        self.assertEqual(resp_get_all_comment_reply_likes.status_code, 200)

    def test_delete_reply_like_succeeds(self):
        """
        Test get all likes a specific comment reply
        Returns:
             200 status code if all likes are returned 
        """
        self.comment_id = self.testcomment.pk
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comment-reply', args=[self.slug, self.comment_id]), content_type='application/json',
                                HTTP_AUTHORIZATION='Bearer ' + self.test_user_token, data=json.dumps(test_data.commentReply_data['reply_data']))
        self.reply_id = resp.data['reply']['id']

        resp_like_comment_reply = self.client.put(reverse('comments:comment-reply-like', args=[self.slug, self.comment_id, self.reply_id]), content_type='application/json', data=json.dumps({}),
                                                  HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)

        resp_delete_reply_like = self.client.delete(reverse('comments:comment-reply-like', args=[
                                                    self.slug, self.comment_id, self.reply_id]), HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        self.assertEqual(resp_delete_reply_like.status_code, 200)

    def test_unlike_reply_like_fails_if_reply_not_liked(self):
        """
        Test get all likes a specific comment reply
        Returns:
             200 status code if all likes are returned 
        """
        self.comment_id = self.testcomment.pk
        self.slug = self.created_article.slug
        resp = self.client.post(reverse('comments:comment-reply', args=[self.slug, self.comment_id]), content_type='application/json',
                                HTTP_AUTHORIZATION='Bearer ' + self.test_user_token, data=json.dumps(test_data.commentReply_data['reply_data']))
        self.reply_id = resp.data['reply']['id']

        resp_delete_reply_like = self.client.delete(reverse('comments:comment-reply-like', args=[
                                                    self.slug, self.comment_id, self.reply_id]), HTTP_AUTHORIZATION='Bearer ' + self.test_user_token)
        self.assertEqual(resp_delete_reply_like.status_code, 400)
