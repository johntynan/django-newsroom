from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.base import ModelBase
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField

from multimedia.constants import MEDIA_TYPES, MEDIA_STATUS_CHOICES, MEDIA_STATUS_DRAFT
from utils.model_inheritance import ParentModel,ChildManager
from videos.models import Video as VideoModel

class MediaBase(ModelBase):
    def __init__(cls, name, bases, attrs):
        #TODO register the incoming media types
        pass
    
class MediaAttribute(object):
    """
    A descriptor that allows Media properties to look for the
    property name on the underlying content object (the generic relation)
    If the content object contains the attribute, return it from there, otherwise
    return from the Media instance
    """
    def __init__(self,**kwargs):
        self.name = kwargs.get('fn')
        self.attrname = kwargs.get('syn',self.name)
    
    def __get__(self,obj,type=None):
        if hasattr(obj.content_object,self.name):
            return getattr(obj.content_object,self.name)
        else:
            return getattr(obj,'m_%s'%self.attrname)
    
    def __set__(self,obj,value):
        if hasattr(obj.content_object,self.name):
            setattr(obj.content_object,self.name)
        else:
            setattr(obj,'m_%s'%self.attrname)
    
    

class Media(ParentModel):
    """
    A generic container for media items.
    
    
    """
    __metaclass__ = MediaBase
    
    m_owners = models.ManyToManyField(User)
    m_title = models.CharField(max_length=128,blank=True)
    m_summary = models.TextField(blank=True)
    m_tags = TagField()
    m_status = models.CharField(
                        max_length=1,
                        choices=MEDIA_STATUS_CHOICES,
                        default=MEDIA_STATUS_DRAFT,
                        help_text=_(u'Only published items will appear on the site.'),)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    #these are the "public" attributes 
    owners = MediaAttribute(fn="authors",syn="owners")
    title = MediaAttribute(fn="title")
    summary = MediaAttribute(fn="summary")
    tags = MediaAttribute(fn="tags")
    status = MediaAttribute(fn="status")
    #preview = MediaAttribute(fn="preview")
    
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

    def get_insert_snippet(self):
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
    media_type = "image"
    
    def render(self,*args,**kwargs):
        return u'<img src="%s"/>' % self.content_object.image.url
    
class Video(Media):
    """
    A Media container for Video instances
    """
    media_type = "video"
    
    #preview = MediaAttribute(fn="frame.image")
    
def associate_video(sender,**kwargs):
    if kwargs.get('created',False):
        video = Video()
        video.content_object = kwargs.get('instance')
        video.save()

post_save.connect(associate_video,VideoModel)   
        
