from django import template
from django.template import TemplateSyntaxError
from multimedia.models import Media

register = template.Library()

class MediaNode(template.Node):
    def __init__(self,media_id):
        self.media_id = template.Variable(media_id)
        
    def render(self,context):
        media_id = self.media_id.resolve(context)
        media = Media.objects.get(pk=media_id)
        as_child = media.get_child_object()
        return as_child.render()

@register.tag
def media_insert(parser,token):
    """
    A tag that renders a media item
    """
    
    args = token.split_contents()
    if len(args) < 2:
        raise TemplateSyntaxError("media_insert tag must have at least one argument")
    media_id = args[1]
    return MediaNode(media_id)

