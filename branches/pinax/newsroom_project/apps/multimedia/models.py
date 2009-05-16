# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

from django.db import models
from django.db.models.base import ModelBase
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from tagging.fields import TagField

from multimedia.constants import LICENSE_CHOICES, LICENSE_DEFAULT
from utils.model_inheritance import ParentModel,ChildManager


class _MediaTypesDescriptor(object):
    def __get__(self,obj,type=None):
        return type._media_types.keys()
    def __set__(self,obj,value):
        raise NotImplementedError

class MediaBase(ModelBase):
    def __init__(cls, name, bases, attrs):
        """
        Registers the media types with the class. Media will
        have a list of all known media types in the media_types list attribute. Ex:

        In [1]: from multimedia.models import Media

        In [2]: Media.media_types
        Out[2]: ['Image', 'Video']

        Additionally, each subclass of Media will have a media_type attribute
        indicating the media type string registered with Media. By default this is just
        the class name, but it can be overridden by explicitly adding a media_type attribute
        to subclass definitions.

        """
        #TODO: media_type doesn't work for Media instances (subclasses OK)

        if not hasattr(cls,'_media_types'):
            setattr(cls,'_media_types',dict())
            setattr(cls,'media_types',_MediaTypesDescriptor())
        else:
            if hasattr(cls,'media_type'):
                cls._media_types[name] = cls
            else:
                setattr(cls,'media_type',name)
                cls._media_types[name] = cls
        #super(MediaBase,cls).__init__(cls,name,bases,attrs)



class MediaManager(models.Manager):

    def published(self):
        return self.filter(status=MEDIA_STATUS_PUBLISHED)


class Media(ParentModel):
    """
    A generic container for media items.

    Subclasses should provide any specific fields they need for managing their
    media type.
    """
    __metaclass__ = MediaBase
    sites = models.ManyToManyField(Site, verbose_name=_(u'Sites'))
    authors = models.ManyToManyField(User)
    title = models.CharField(max_length=128,)
    summary = models.TextField(blank=True)
    attribution = models.TextField(blank=True)
    tags = TagField()
    license = models.CharField(
                        max_length=100,
                        choices = LICENSE_CHOICES,
                        default=LICENSE_DEFAULT,
                        help_text=_(u'Choose the license you wish to publish this work under.'),)
    slug = models.SlugField(
                    _(u'Slug'),
                    help_text=_(u'Automatically built from the title.'),)
    pub_date = models.DateTimeField(
                    _(u'Date published'),
                    default=datetime.datetime.now,
                    help_text=_(u'Publication date'),)

    # not sure how use these fields in a subclass, django gives an error.
    #created_by = models.ForeignKey(
    #                        User,
    #                        related_name="media_created")
    #
    #modified_by = models.ForeignKey(
    #                        User,
    #                        related_name="media_modified")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = MediaManager()
    children = ChildManager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name_plural = 'Media'
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return self.title

    @staticmethod
    def class_factory(media_type):
        return Media._media_types[media_type.capitalize()]


    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Media,self).save()

    def get_thumbnail_url(self):
        """
        return the absolute path to the default thumbnail.
        Subclasses should implement this
        """
        child = self.get_child_object()
        if hasattr(child,'get_thumbnail_url'):
            return self.get_child_object().get_thumbnail_url()
        else:
            return "%simages/generic_thumbnail.png" % settings.MEDIA_URL

    def get_height(self):
        """
        Return integer or None
        """
        child = self.get_child_object()
        if hasattr(child, 'get_height'):
            return child.get_height()
        else:
            return None

    def get_height_with_margin(self):
        """
        Return integer or None
        """
        return self.get_height() + 20

    def get_width(self):
        """
        Return integer or None
        """
        child = self.get_child_object()
        if hasattr(child, 'get_width'):
            return child.get_width()
        else:
            return None

    def get_width_with_margin(self):
        """
        Return integer or None
        """
        return self.get_width() + 20


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
            return '{%% media_insert %d "%s" %%}' % (self.id,self.title)
        else:
            return "{%% media_insert %d "" %%}" % self.id

    def get_parent_model(self):
        """
        Helper method for inheritance
        """
        return Media

    def get_absolute_url(self):
        return reverse('multimedia_detail',
                       dict(media_id=self.id,slug=self.slug))

    def get_media_type(self):
        """
        Return lowercase string the matches media type.
        """
        return self.get_child_object().media_type.lower()

