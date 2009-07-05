import os
import zipfile
from zipfile import BadZipfile
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from multimedia.models import Media
from imagekit.models import ImageModel


IK_SPEC_MODULE = getattr(settings, 'FLASHPROJECTS_IMAGEKIT_SPEC', 'flashprojects.ik_specs')
    
class PosterFrame(ImageModel):
    """
    ImageModel that will define the poster frame of the flash project.
    """

    image = models.ImageField(
        'Poster Frame',
        upload_to='uploads/flashprojects/%Y/%m/%d/',
        max_length=255,
        help_text="An image that can be used to reference the project.")

    def __unicode__(self):
        return self.image.name

    class IKOptions:

        spec_module = IK_SPEC_MODULE
        cache_dir = 'ik_cache/flashprojects'
        cache_filename_format = "%(specname)s/%(filename)s.%(extension)s"


class FlashProject(Media):
    

    loader_swf = models.CharField(
                    max_length=255, 
                    help_text="Full path to the swf used to start the flash movie.",
                    blank=True)

    width = models.CharField(
                max_length=4,
                help_text='Width of the flash movie in pixels.')
    height = models.CharField(
                max_length=4,
                help_text='Height of the flash movie in pixels.')
    flash_compat = models.CharField(
                        "Flash Compatibility",
                        choices = (
                            ('6','6'), 
                            ('7','7'), 
                            ('8','8'), 
                            ('9','9'),
                            ('10','10')),
                        max_length=5,
                        default='9',
                        help_text="Please select the lowest version of Flash this project is compatible with.")
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

    zip_file = models.FileField(
                    upload_to='uploads/flashprojects/%Y/%m/%d/',
                    storage=FileSystemStorage(),
                    help_text='Zip file containing a subdirectory with flash project inside of it.')


    #def save(self, *args, **kwargs):
    #    """
    #    Unpack the zip file and delete it after successful save.
    #    """
    #    super(FlashProject, self).save(*args, **kwargs)
    #    self.process_zipfile()

    def get_project_dir(self):
        """
        Return directory where loader swf can find referenced files.  
        Useful in base param on flash embeds.
        """
        pass
        
    def process_zipfile(self):
        """
        Extract the files into a location and match the loader.
        """
        if os.path.isfile(self.zip_file.path):
            try:
                zip = zipfile.ZipFile(self.zip_file.path)
                #import ipdb
                #ipdb.set_trace()
            except BadZipfile:
                self.zip_file.delete()
                raise BadZipfile, "File is not a zip file."

            #bad_file = zip.testzip()
            #if bad_file:
            #    raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_thumbnail_url(self):
        return self.poster_frame.mediumthumb.url

    def get_original_url(self):
        try:
            return self.zip_file.url
        except ValueError:
            pass

