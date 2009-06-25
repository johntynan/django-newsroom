from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
#from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from tagging.models import Tag
from tagging.fields import TagField
from imagekit.models import ImageModel
from multimedia.models import Media


IK_SPEC_MODULE = getattr(settings, 'VIDEOS_IMAGEKIT_SPEC', 'videos.ik_specs')

class VideoManager(models.Manager):
    pass

class VideoFrame(ImageModel):
    """
    Define ImageModel that will define the first frame and thumbnails
    of a video.
    """
    
    image = models.ImageField(
        upload_to='uploads/videos/%Y/%m/%d/',
        max_length=255)

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
                        help_text=_(u'Select the video for upload, supported encodings are h.264 and flash video.'),
                        max_length=255)

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

    def get_display140_url(self):
        return self.frame.display140.url

    def get_width(self):
        return self.frame.image.width

    def get_width_with_margin(self):
        return self.get_width() + 20

    def get_height(self):
        return self.frame.image.height

    def get_height_with_margin(self):
        return self.get_height() + 50

    def get_original_url(self):
        return self.video.url

    #TODO update this
    def get_absolute_url(self):
        return ('videos_video_detail', 
                (), 
                { 'video_id': self.id, 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)

