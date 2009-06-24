from django.db import models

class FlashArchive(models.Model):
    title = models.CharField(
                "Folder Name",
                max_length=255) 
    file = models.FileField(upload_to='flash')

    def __unicode__(self):
        return self.title

    
class Flash(models.Model):
    title = models.CharField(
                "Flash Project",
                max_length=255)
    width = models.CharField(max_length=5)
    height = models.CharField(max_length=5)
    embed = models.TextField(
                "Embed / HTML",
                blank=True,
                help_text="HTML Embed for Flash",)

    flash_archive = models.ForeignKey(
                FlashArchive,
                help_text="Flash archive associated with a flash project.",)

    def __unicode__(self):
        return self.title

class FlashObject(models.Model):
    title = models.CharField(
                "Filename",
                max_length=255)
    flash_version = models.CharField(
                "Flash Version",
                max_length=255)
    object_id = models.CharField(
                "Object ID",
                max_length=255)
    flash = models.ForeignKey(
                Flash,
                help_text="Flash Project associated with this flash object.",)
                
    def __unicode__(self):
        return self.title