import os
import zipfile
from zipfile import BadZipfile
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
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
                    help_text="Path to the swf used to start the flash movie.")

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
                    help_text='Zip file containing a subdirectory with flash project inside of it.',
                    max_length=200)


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

        zf = None
        workingdir = ''

    #if os.path.isfile(self.zip_file.path):
        try:
            zf = zipfile.ZipFile(self.zip_file.path)
            #import ipdb; ipdb.set_trace()
        except BadZipfile:
            self.zip_file.delete()
            raise BadZipfile, "File is not a zip file."

        workingdir = os.path.join( 
                        os.path.dirname(zf.filename), 
                        slugify(self.title))

        bad_file = zf.testzip()
        if bad_file:
            raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)

        if not os.path.isdir(workingdir):
            # TODO move dir if it exists
            os.mkdir(workingdir)

        for name in zf.namelist():

            newfile = os.path.join(workingdir, name)
            
            if newfile.endswith(os.path.sep):
                if not os.path.isdir(newfile):
                    os.mkdir(newfile)

            else:
                data = zf.read(name)
                tempdata = open(newfile, "wb")
                tempdata.writelines(data)
                tempdata.close()

        zf.close()
        #print '!!!!!!!!!'
        #print 'unzipped '+str(zf)
        #print '!!!!!!!!!'

    def get_width(self):
        return self.width

    def get_width_with_margin(self):
        return int(self.get_width()) + 20

    def get_height(self):
        return self.height

    def get_height_with_margin(self):
        return int(self.get_height()) + 40

    def get_thumbnail_url(self):
        return self.poster_frame.mediumthumb.url

    def get_loader_url(self):
        """
        Return relative URL to loader swf
        """
        return '%s/%s/%s' % (os.path.dirname(self.zip_file.url),
                                 slugify(self.title),
                                 self.loader_swf)

    def get_render_url(self):
            return reverse('multimedia_preview', args=[self.id])

