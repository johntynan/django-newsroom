from django.db import models


class Flash(models.Model):
    title = models.CharField(max_length=255)    

    def __unicode__(self):
        return self.title

class FlashArchive(models.Model):
    title = models.CharField(max_length=255) 
    file = models.FileField(upload_to='flash')


    flash = models.ForeignKey(
                Flash,
                help_text="Flash archive associated with a flash object.",)

    def __unicode__(self):
        return self.title