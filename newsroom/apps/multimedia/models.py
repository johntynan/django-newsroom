from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models


class Media(models.Model):
    """
    A generic container for media items.
    """
    quicktag = models.CharField(max_length=32)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def render_media(self):
        """
        Handles rendering of the encapsulated media object to HTML
        """
        pass

    def get_insert_snippet(self,args,**kwargs):
        """
        Creates the text snippet that Story authors will paste into their content to indicate that the
        media item should render should render itself there.
        
        """
        pass
    