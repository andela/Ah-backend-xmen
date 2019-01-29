from authors.apps.utils.renderers import AppJSONRenderer

import json

from rest_framework.renderers import JSONRenderer

class UserProfileJSONRenderer(AppJSONRenderer):
    name = 'profile'

class UserProfileListRenderer(JSONRenderer):
    """
    Returns profiles of existing users
    """
    charset = 'utf-8'
    
    def render(self, data, media_type=None, renderer_context=None):
        """ present a list of 
        user profiles in json format
        """
        return json.dumps({
            'profiles':data
        })
