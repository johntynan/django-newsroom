from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from tagging.models import Tag
from tagging.fields import TagField
from videos.constants import VIDEO_STATUS_CHOICES, VIDEO_STATUS_DRAFT, VIDEO_STATUS_PUBLISHED
from imagekit.models import ImageModel


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



class Video(models.Model):
    """
    Define a video object.
    """

    site = models.ForeignKey(Site, verbose_name=_(u'Site'),) 

    authors = models.ManyToManyField(User)


    status = models.CharField(
                        max_length=1,
                        choices=VIDEO_STATUS_CHOICES,
                        default=VIDEO_STATUS_DRAFT,
                        help_text=_(u'Only published videos will appear on the site.'),)

    video = models.FileField(
                        upload_to='uploads/videos/%Y/%m/%d/', 
                        verbose_name=_(u'Video file'),
                        help_text=_(u'Select the video for upload.'),)

    frame = models.ForeignKey(
                    VideoFrame, 
                    verbose_name=_(u'First Frame'),
                    blank=True, 
                    null=True,
				    help_text=_(u'One frame or image that represents the video.  Should be same width/height as the video.'),)

    title = models.CharField(_(u'Title'), max_length=80,)

    slug = models.SlugField(
                    _(u'Slug'),
                    help_text=_(u'Automatically built from the title.'),)

    summary = models.TextField(_(u'Summary'), blank=True, null=True, ),

    #tags = TagField(verbose_name=_(u'Tags'), blank=True, null=True, 
	#            help_text=_(u'Separate tags with spaces or commas.'))
    tag_list = models.CharField(max_length=250)

    pub_date = models.DateTimeField(
                    _(u'Date published'), 
                    default=datetime.now, 
				    help_text=_(u'Publication date of the video.'),)

    created_by = models.ForeignKey(
                            User, 
                            related_name="videos_created")

    modified_by = models.ForeignKey(
                            User, 
                            related_name="videos_modified")

    created = models.DateTimeField(default=datetime.now)

    modified = models.DateTimeField(auto_now=True)
    
    objects = VideoManager()

    def _get_tags(self):
        return Tag.objects.get_for_object(self)
    def _set_tags(self, tag_list):
        Tag.objects.update_tags(self, tag_list)
    tags = property(_get_tags, _set_tags)

    class Meta:
        verbose_name_plural = _(u'videos')
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return self.title

    def save(self):
        super(Video, self).save()
        Tag.objects.update_tags(self, self.tag_list)

    def get_absolute_url(self):
        return '/videos/%s/%s/' % (self.pub_date.strftime("%Y/%b/%d").lower(),
                                    self.slug)
