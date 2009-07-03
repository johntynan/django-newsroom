from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from multimedia.models import Media
from imagekit.models import ImageModel

IK_SPEC_MODULE = getattr(settings, 'FLASHPROJECTS_IMAGEKIT_SPEC', 'flashprojects.ik_specs')
    
class PosterFrame(ImageModel):
    """
    ImageModel that will define the poster frame of the flash project.
    """

    image = models.ImageField(
        upload_to='uploads/flashprojects/%Y/%m/%d/',
        max_length=255)

    def __unicode__(self):
        return self.image.name

    class IKOptions:

        spec_module = IK_SPEC_MODULE
        cache_dir = 'ik_cache/flashprojects'
        cache_filename_format = "%(specname)s/%(filename)s.%(extension)s"


class FlashProject(Media):
    
    zip_file = models.FileField(
                    upload_to='uploads/flashprojects/%Y/%m/%d/')

    loader_swf = models.CharField(
                    max_length=255, 
                    help_text="Full path to the swf used to start the flash movie.",
                    blank=True)

    width = models.CharField(max_length=4)
    height = models.CharField(max_length=4)
    flash_version = models.CharField(
                        choices = (
                            ('6','6'), 
                            ('7','7'), 
                            ('8','8'), 
                            ('9','9'),
                            ('10','10')),
                        max_length=5,
                        default='9',
                        help_text="Please select the lowest version of flash this project is compatible with.")
    created_by = models.ForeignKey(
                            User,
                            related_name="flashprojects_created")
    modified_by = models.ForeignKey(
                            User,
                            related_name="flashprojects_modified")
    poster_frame = models.ForeignKey(
                            PosterFrame, 
                            blank=True, 
                            null=True,
                            help_text="An image that can be used to reference the project.")

    #def save(self, *args, **kwargs):
    #    self.process_zipfile()
    #    super(FlashProject, self).save(*args, **kwargs)
    #    super(GalleryUpload, self).delete()
    #    return gallery

    def process_zipfile(self):
        """
        Extract the zip file into a temporary location and match the loader 
        """
        pass


    def get_project_dir(self):
        """
        Return directory where loader swf can find referenced files.  
        Useful in base param on flash embeds.
        """
        pass
        
