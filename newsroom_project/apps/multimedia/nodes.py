from django.core.exceptions import ObjectDoesNotExist
from django import template
from django.template.loader import get_template
from multimedia.models import Media

class MediaNode(template.Node):
    """
    A template Node that attempts to lookup a Media object
    by id and render it using its Media type's template.
    Renders an empty string if the Media object is not found.
    """
    def __init__(self,media_id):
        self.media_id = template.Variable(media_id)
        
    def render(self,context):
        media_id = self.media_id.resolve(context)
        try:
            media = Media.objects.get(pk=media_id)
        except ObjectDoesNotExist:
            return ''
            
        as_child = media.get_child_object()
        template = get_template('multimedia/render/%s.html' % as_child.media_type.lower())
        return template.render(context)