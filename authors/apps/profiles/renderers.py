import json

from rest_framework.renderers import JSONRenderer


class UserProfileJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        errors = data.get('errors', None)

        if errors is not None:
            # As mentioned about, we will let the default JSONRenderer handle
            # rendering errors.
            return super(UserProfileJSONRenderer, self).render(data)

        # Finally, we can render our data under the "user" namespace.
        return json.dumps({
            'profile': data
        })

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
