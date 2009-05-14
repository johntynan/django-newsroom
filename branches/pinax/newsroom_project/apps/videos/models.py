from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
#from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from tagging.models import Tag
from tagging.fields import TagField
from multimedia.constants import MEDIA_STATUS_PUBLISHED
from imagekit.models import ImageModel
from multimedia.models import Media


IK_SPEC_MODULE = getattr(settings, 'VIDEOS_IMAGEKIT_SPEC', 'videos.ik_specs')

class VideoManager(models.Manager):

    def published(self, **kwargs):
        return self.filter(status=MEDIA_STATUS_PUBLISHED, **kwargs)

class VideoFrame(ImageModel):
    """
    Define ImageModel that will define the first frame and thumbnails
    of a video.
    """
    
    image = models.ImageField( upload_to='uploads/videos/%Y/%m/%d/',) 

    def __unicode__(self):
        return self.image.name

    class IKOptions:

        spec_module = IK_SPEC_MODULE
        cache_dir = 'ik_cache/videos'
        cache_filename_format = "%(specname)s/%(filename)s.%(extension)s"


class Video(Media):
    """
    Define a video object.
    """

    video = models.FileField(
                        upload_to='uploads/videos/%Y/%m/%d/', 
                        verbose_name=_(u'Video file'),
                        help_text=_(u'Select the video for upload, supported encodings are h.264 and flash video.'),)

    frame = models.ForeignKey(
                    VideoFrame, 
                    verbose_name=_(u'First Frame'),
                    blank=True, 
                    null=True,help_text=_(u'One frame or image that represents the video.  Should be same width/height as the video.'))

    created_by = models.ForeignKey(
                            User, 
                            related_name="videos_created")

    modified_by = models.ForeignKey(
                            User, 
                            related_name="videos_modified")

    class Meta:
        verbose_name_plural = _(u'videos')

    def get_thumbnail_url(self):
        return self.frame.mediumthumb.url

    def get_width(self):
        return self.frame.image.width

    def get_height(self):
        return self.frame.image.height

    #TODO update this
    def get_absolute_url(self):
        return ('videos_video_detail', 
                (), 
                { 'video_id': self.id, 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)

