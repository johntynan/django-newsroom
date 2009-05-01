from django import template
from django.template import TemplateSyntaxError
#from django.template.loader import get_template
#from multimedia.models import Media
from multimedia.nodes import MediaNode

register = template.Library()

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

