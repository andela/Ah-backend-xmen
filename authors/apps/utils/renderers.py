import json
from rest_framework.renderers import JSONRenderer


class AppJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    name = 'app'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({
            self.name: data
        })
