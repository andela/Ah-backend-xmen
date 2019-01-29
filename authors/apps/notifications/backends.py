from .models import Notification
from django.urls import reverse
from .utils import permissions
from authors.apps.core.models import email_dispatch
import threading


class NotificationDispatch:
    def profile_followed(self, request, followed_profile):
        """
        notify users of new followers on their profiles

        Args:
            request(Request): request object of the follower
            followed_profile(ProfileModel):

        """
        follower_profile = request.user.profile
        if permissions.PROFILE_FOLLOW \
                not in followed_profile.notification_perms or \
                self._is_same_profile(followed_profile, follower_profile):
            return
        full_name = self._get_name(follower_profile)
        action_link = request.build_absolute_uri(
                            reverse('profiles:profile-detail',
                                    kwargs={
                                     'username': follower_profile.user.username
                                      }))
        message = full_name + " has started following you."
        self._dispatch(request, (follower_profile,
                                 followed_profile, message,
                                 action_link, ),
                       permissions.PROFILE_FOLLOW)

    def article_created(self, request, article):
        """ 
        notify author's followers about creation of new articles.

        Args:
            request (Request); request object of the author
            article (ArticleModel): The article object

        """
        people_to_notify = []
        for person in article.author.followers.all():
            if permissions.FOLLOWED_AUTHOR_ARTICLE_CREATED in \
                    person.profile.notification_perms:
                people_to_notify.append(person.profile)
        for person in people_to_notify:
            action_link = request.build_absolute_uri(
                reverse('articles:article-update',
                        kwargs={'slug': article.slug}))

            message = self._message_builder(article.author,
                                            "published a new article",
                                            article.title)
            self._dispatch(request,
                           (article.author, person, message, action_link,),
                           permissions.FOLLOWED_AUTHOR_ARTICLE_CREATED)

    def article_interaction_comment(self, request, comment):
        """
        notify users that created or favorited an article of
        a new comment

        args:
            request (Request): the commenter's request object
            comment (CommentModel): The comment object

        """
        sender = comment.author
        receiver = comment.article.author
        if self._is_same_profile(sender, receiver):
            return
        message = self._message_builder(sender,
                                        "left a  comment on your article",
                                        comment.article.title
                                        )
        action_link = request.build_absolute_uri(reverse(
            'comments:comment-detail', 
            kwargs={'slug': comment.article.slug, 'pk': comment.pk}))
        self._dispatch(request, (sender,
                       receiver, message, action_link,),
                       permissions.AUTHORED_ARTICLE_COMMENTED)

        for profile in comment.article.favorites.all():
            if permissions.FAVORITED_ARTICLE_COMMENTED in profile.notification_perms:
                message = self._message_builder(
                    sender, "left a  comment on an article you favorited,",
                    comment.article.title
                )
                profile.user.email
                self._dispatch(request, (sender,
                               profile, message, action_link,),
                               permissions.FAVORITED_ARTICLE_COMMENTED)

    def article_interaction_liked_or_faved(
            self, request, article, liked_by=None, favorited_by=None):
        """
        notify users that created an article of
        a new like or favorite

        args:
            request (Request): the commenter's request object
            article(ArticleModel): the article object
            liked_by (ProfileModel): the liker's profile object, Defaults to None
            favorited_by (ProfileModel): the favoriter's profile object, Defaults to None  

        """
        sender = liked_by or favorited_by
        receiver = article.author

        if self._is_same_profile(sender, receiver):
            return
        
        action_link = request.build_absolute_uri(
            reverse('articles:article-update', kwargs={'slug': article.slug}))
           
        if liked_by is not None:
            message = self._message_builder(sender,
                                            "liked your article",
                                            article.title
                                            )
        
            self._dispatch(request, (sender,
                           receiver, message, action_link,),
                           permissions.AUTHORED_ARTICLE_LIKED)
       
        if favorited_by is not None:
            sender_profile = sender
            message = self._message_builder(sender_profile,
                                            "favorited your article",
                                            article.title
                                            )
         
            self._dispatch(request, (sender,
                           receiver, message, action_link,),
                           permissions.AUTHORED_ARTICLE_FAVORITED)

    def _is_same_profile(self, sender, receiver):
        """
        checks if sender profile is receiver profile

        Args:
            sender (ProfileModel): the sender's profile
            receiver (ProfileModel): the receiver's profile

        return True or False

        """
        return sender.user.username == receiver.user.username

    def _message_builder(self, person, message, title):
        """
        builds a notification message string
        Args:
            person(ProfileModel): person mentioned in the notification
            message(String): message describing changes
            title(String): affected article title

        returns:
            notification_message(String)
        """
        return self._get_name(person)\
            + " " + message+",  "+title

    def _dispatch(self, request, notification, permission_type):
        sender, receiver, message, action_link = notification
        if permission_type in receiver.notification_perms:
            notification = Notification.objects.create_notification(
                sender=sender,
                receiver=receiver,
                message=message,
                action_link=action_link
                )
        if permissions.RECEIVE_NOTIFICATION_EMAILS in receiver.notification_perms:
            
            thread = threading.Thread(target=email_dispatch.build_and_send,
                                      args=[request, notification,
                                            permission_type])
            thread.setDaemon(True)
            thread.start()

    def _get_name(self, sender):
        """
        Builds a person's name from a ProfileModel object.
        
        Args:
            sender(ProfileModel): the sender's object
        
        returns:
            name(String); sender's full name or username

        """

        return "{} {}".format(sender.first_name, sender.last_name) \
            if sender.first_name is not None and sender.last_name is not None \
            else sender.user.username


notify = NotificationDispatch()
