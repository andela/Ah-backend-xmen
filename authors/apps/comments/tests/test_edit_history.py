from authors.apps.authentication.tests_ import test_base_class
from django.shortcuts import reverse
import json
from authors.apps.authentication.tests_ import test_data


class TestCommentHistoryEndpoint(test_base_class.BaseTestClass):

    def test_fetch_comment_history_succeeds(self):
        """
        Tests successful fetch of comment history
        """
        self.slug = self.created_article.slug
        resp_1 = self.client.post(
            reverse('comments:comments', args=[self.slug]),
            content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token,
            data=json.dumps(test_data.comment_data['comment_data']))
        self.comment_id = resp_1.data['comment']['id']
        self.client.put(
            reverse('comments:comment-detail',
                    args=[self.slug, self.comment_id]),
            content_type='application/json', HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token,
            data=json.dumps(test_data.comment_data['comment_update']))
        resp_3 = self.client.get(
            reverse('comments:comment-history',
                    args=[self.slug, self.comment_id]),
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        self.assertEqual("update",
                         resp_3.data["comment_history"][0].get(
                             'history_change_type'))


class TestReplyHistoryEndpoint(test_base_class.BaseTestClass):

    def test_fetch_reply_history_succeeds(self):
        """
        Tests successful fetch of comment reply history
        """
        self.comment_id = self.testcomment.pk
        self.slug = self.created_article.slug
        resp = self.client.post(
            reverse('comments:comment-reply',
                    args=[self.slug, self.comment_id]),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token,
            data=json.dumps(test_data.commentReply_data['reply_data']))
        self.reply_id = resp.data['reply']['id']
        self.client.put(
            reverse('comments:comment-reply-detail',
                    args=[self.slug, self.comment_id, self.reply_id]),
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token, content_type='application/json',
            data=json.dumps(
                test_data.commentReply_data['reply_update_data']))
        resp_4 = self.client.get(
            reverse('comments:reply-history',
                    args=[self.slug, self.comment_id, self.reply_id]),
            HTTP_AUTHORIZATION='Bearer ' +
            self.test_user_token)
        self.assertEqual("update",
                         resp_4.data["reply_history"][0].get(
                             'history_change_type'))
