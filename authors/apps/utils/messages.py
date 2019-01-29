

error_messages = {
    'field required': '{} is required.',
    'permission_denied': "You do not have permission to perform this action",
    'delete_msg': "{} successfully deleted",
    'follow denied':'You cannot follow yourself.',
    'unfollow denied':'You cannot unfollow yourself.', 
    'already follow':'You already follow {}', 
    'not follow': 'You do not follow {}',
    'already_reported': 'This article has already been reported, action is being taken'
}

response = {
    'follow message': 'You have followed {}', 
    'unfollow message': 'You have unfollowed {}'
}


favorite_actions_messages = {
    'favorited':'Article has been added to favorites',
    'already_favorited':'Article already in favorites',
    'un_favorited': 'Article has been removed from favorites',
    'not_favorited':'Article does not exist in your favorites'
}

notification_mesages = {
    'missing_field': 'Notification must have a valid {}'
}


tasks = {
    'all': 'all',
    'unread': 'unread'
}
escalation_message = """
    {} has reported this article 
    {}
    for violating authors heaven terms.

    REASON.
    {}.
    Please review and take action!
    """
