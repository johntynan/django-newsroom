from django.db import models
from photos.models import Photo

class PageLayout(models.Model):
    """
    PageLayouts are...
    
    """
    title = models.CharField(max_length=256)
    html = models.TextField()
    description = models.TextField()
    image = models.CharField(max_length=256)
    
    def __unicode__(self):
        return self.title

