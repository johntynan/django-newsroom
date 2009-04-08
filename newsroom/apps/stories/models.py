import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save,post_delete
from multimedia.models import Media
from stories.constants import STORY_STATUS_CHOICES, STORY_STATUS_DRAFT

class Story(models.Model):
    """
    A Story is composed of one or more Pages
    """
    authors = models.ManyToManyField(User)
    headline = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    lead_art = models.ForeignKey(Media,null=True,blank=True)
    summary = models.TextField(blank=True)
    status = models.CharField(max_length=1,choices=STORY_STATUS_CHOICES,default=STORY_STATUS_DRAFT)
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(auto_now=True)
    
    @property
    def pages(self):
        return self.page_set.all()
        
    @property
    def page_one(self):
        return self.get_page(1)
        
    def get_page(self,num):
        return self.page_set.get(pagenum=num)
        
    def add_page(self):
        """
        Creates a new page for this story. Returns the newly created page
        """
        new_page = Page.objects.new_page(self)
        self.page_set.add(new_page)
        return new_page

        
def new_story_add_page(sender,**kwargs):
    """
    Post-save signal for Story.
    All stories should have at least one page. 
    """
    story = kwargs.get('instance',None)
    new = kwargs.get('created',False)
    if new and story:
        story.add_page()
        
post_save.connect(new_story_add_page,sender=Story)

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

class StoryIntegrityError(Exception):
    """
    This exception should be raised when an application attempts to
    delete the only Page associated with a Story instance.
    """
    pass

class Page(models.Model):
    """
    A Page represents a 'section' of a Story
    """
    story = models.ForeignKey(Story)
    content = models.TextField()
    media = models.ManyToManyField(Media)
    pagenum = models.PositiveIntegerField()
    
    objects = PageManager()
    
    class Meta:
        ordering = ('pagenum',)
        
    def __unicode__(self):
        return u"%s: Page %d" % (self.story.headline,self.pagenum)
    
    def delete(self):
        """
        Re-orders the remaining pages
        """
        #don't delete if this is the only Page associated with a Story
        if self.story.pages.count() == 1:
            raise StoryIntegrityError
        super(Page,self).delete()
        

def reorder_story_pages(sender,**kwargs):
    story = kwargs['instance'].story
    Page.objects.update_page_order(story)
    
post_delete.connect(reorder_story_pages,Page)

