from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.signals import post_save

from multimedia.constants import MEDIA_TYPES
from utils.model_inheritance import ParentModel,ChildManager

class Media(ParentModel):
    """
    A generic container for media items.
    
    
    """
    owners = models.ManyToManyField(User)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    #media_type = models.CharField(max_length=24,choices=MEDIA_TYPES)
    
    #def __unicode__(self):
    #    """
    #    experimental: output self as HTML ala Django Forms
    #    so that template authors can do things like
    #    {{some_instance.media}}
    #    """
    #    pass
        
    objects = models.Manager()
    children = ChildManager()
    
    def get_parent_model(self):
        return Media

    def render(self,*args,**kwargs):
        """
        Handles rendering of the encapsulated media object to HTML
        
        Must be implemented by subclass
        """
        raise NotImplentedError

    def get_insert_snippet(self,args,**kwargs):
        """
        Creates the text snippet that Story authors will paste into their content to indicate that the
        media item should render should render itself there.
        
        The most basic form of the tag will look like
        
            {% media_insert <media_id> %}
            
        where media_id is the id of a Media object.
        
        If the user supplied a title with the media item, we tack that in as a convenience so that authors
        can quickly identify which media item will be shown when they are editing stories.
        An example snippet might then look like:
            
            {% media_insert 364 "obama speaking" %}
        
        Individual media types may desire/require arbitrary parameters for initializing/customizing the media
        object. Media subclasses should override this method so that they can translate additional arguments
        into the snippet in a way that the render method will be able to leverage.
        """
        if len(self.title):
            return '{%% media_insert %d "%s" %%}' % (self.id,self.title,)
        else:
            return "{%% media_insert %d %%}" % self.id
    

class Image(Media):
    """
    A Media container for Photologue Photo instances
    """
    
    #TODO automatically set media type
    
    def render(self,*args,**kwargs):
        return u'<img src="%s"/>' % self.content_object.image.url
        
