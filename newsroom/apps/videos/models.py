from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
#from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from tagging.models import Tag
from tagging.fields import TagField
from videos.constants import VIDEO_STATUS_CHOICES, VIDEO_STATUS_DRAFT, VIDEO_STATUS_PUBLISHED
from imagekit.models import ImageModel
from multimedia.models import Media


IK_SPEC_MODULE = 'videos.photo_specs'

class VideoManager(models.Manager):

    def published(self, **kwargs):
        return self.filter(status=VIDEO_STATUS_PUBLISHED, **kwargs)

class VideoFrame(ImageModel):
    """
    Define ImageModel that will define the first frame and thumbnails
    of a video.
    """
    
    image = models.ImageField( upload_to='uploads/videos/%Y/%m/%d/',) 

    class IKOptions:

        spec_module = IK_SPEC_MODULE
        cache_dir = 'videos'
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

    class Meta:
        verbose_name_plural = _(u'videos')
        

    def get_absolute_url(self):
        return ('videos_video_detail', 
                (), 
                { 'video_id': self.id, 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)


