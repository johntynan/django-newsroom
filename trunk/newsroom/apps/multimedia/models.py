from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

from multimedia.constants import MEDIA_TYPES


class Media(models.Model):
    """
    A generic container for media items.
    """
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    media_type = models.CharField(max_length=24,choices=MEDIA_TYPES)
    
    #def __unicode__(self):
    #    """
    #    experimental: output self as HTML ala Django Forms
    #    so that template authors can do things like
    #    {{some_instance.media}}
    #    """
    #    pass

    def render_media(self,*args,**kwargs):
        """
        Handles rendering of the encapsulated media object to HTML
        """
        raise NotImplentedError

    def get_insert_snippet(self,args,**kwargs):
        """
        Creates the text snippet that Story authors will paste into their content to indicate that the
        media item should render should render itself there.
        
        """
        raise NotImplentedError
    

class Image(Media):
    """
    A Media container for Photologue Photo instances
    """
    def render_media(self,*args,**kwargs):
        return u'<img src="%s"/>' % self.content_object.get_absolute_url()
        
    def get_insert_snippet(self,*args,**kwargs):
        pass
    