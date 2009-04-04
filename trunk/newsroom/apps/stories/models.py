import datetime
from django.contrib.auth.models import User
from django.db import models
from newsroom.multimedia.models import Media
from newsroom.stories.constants import STORY_STATUS_CHOICES

class Story(models.Model):
    """
    A Story is composed of one or more Pages
    """
    author = models.ForeignKey(User)
    headline = models.CharField(max_length=256)
    slug = models.SlugField()
    status = models.CharField(max_length=1,choices=STORY_STATUS_CHOICES)
    summary = models.TextField()
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField()
    
    @property
    def pages(self):
        return self.page_set.all()
        
    def add_page(self):
        return Page.objects.new_page(self)

class PageManager(models.Manager):
    """
    Provides methods that take care of managing the ordering of Pages
    """
    
    def new_page(self,story):
        """
        create a new page with the correct page number assigned
        """
        next_page = self.filter(story=story).count()+1
        return self.create(story=story,pagenum=next_page)
        
    def update_page_order(self,story):
        """
        ensures that there are no gaps in page numbers
        """
        for i,page in enumerate(self.filter(story=story)):
            page.pagenum = i+1
            page.save()

class Page(models.Model):
    """
    A Page represents a 'section' of a Story
    """
    story = models.ForeignKey(Story)
    content = models.TextField()
    media = models.ManyToManyField(Media)
    pagenum = models.PostiveIntegerField()
    
    objects = PageManager()
    
    class Meta:
        ordering = ('pagenum',)
        
    def __unicode__(self):
        return u"%s: Page %d" % (self.story.headline,self.pagenum)
    
    def delete(self):
        """
        Re-orders the remaining pages
        """
        super(Page,self).delete()
        Page.objects.update_page_order(self.story)
    



