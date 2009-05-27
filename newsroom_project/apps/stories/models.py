import re

from django.contrib.auth.models import User
from django.contrib.auth.models import get_hexdigest
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save,post_delete
from django.template import Template, Context
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from multimedia.models import Media
from multimedia.nodes import MediaNode
from topics.models import TopicPath
from stories.constants import STORY_STATUS_CHOICES, STORY_STATUS_DRAFT, STORY_STATUS_PUBLISHED

from supertagging.fields import SuperTagField
from django_inlines import inlines
from django_inlines.samples import YoutubeInline

from geotags.models import Point,Line, MultiLine, Polygon

inlines.registry.register('youtube', YoutubeInline)


class StoryManager(models.Manager):

    def published(self):
        return self.filter(
                    sites__in = [Site.objects.get_current()],
                    status = STORY_STATUS_PUBLISHED,)

class StorySiteManager(models.Manager):
    """
    Custom story manager that always filters querysets based on the sites
    attribute and settings.py of the django project.  This is useful for the
    publication/public facing sites.
    """

    def get_query_set(self):
        return super(StorySiteManager, self).get_query_set().filter(
                    sites__in = [Site.objects.get_current()],)

    def published(self):
        return self.filter(status = STORY_STATUS_PUBLISHED)


class Story(models.Model):
    """
    A Story is composed of one or more Pages
    """
    authors = models.ManyToManyField(User)
    sites = models.ManyToManyField(Site)
    headline = models.CharField(max_length=256)
    slug = models.SlugField(
                unique=True,
                help_text=_("Automatically created based on headline, but you can also specify it."))
    topics = models.ManyToManyField(TopicPath, blank=True)
    lead_art = models.ForeignKey(Media,null=True,blank=True,related_name="lead_art")
    summary = models.TextField(blank=True)
    tags = SuperTagField()
    location = models.CharField(
                max_length=256,
                blank=True,
                help_text=_("City, State Country or Zipcode, Country." ))
    status = models.CharField(max_length=1,choices=STORY_STATUS_CHOICES,default=STORY_STATUS_DRAFT)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True )
    objects = StoryManager()
    on_site = StorySiteManager()
    
    class Meta:
        verbose_name_plural = 'stories'
        ordering = ('creation_date',)
    
    def __unicode__(self):
        return self.headline
        
    @models.permalink
    def get_absolute_url(self):
        return ('stories.views.show_story',[self.slug])
        
    @property
    def pages(self):
        return self.page_set.all()
    @property
    def token(self):
        return get_hexdigest("md5", settings.SECRET_KEY, self.slug)
        
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
        new_page.save()
        self.page_set.add(new_page)
        return new_page

    def get_relatedcontent(self):
        """
        Return a dict where the keys are the verbose_name
        of the RelatedContent class and the items are the
        object list of this particular class.
        """
        relatedcontent_dict = {}
        for relatedcontent in self.relatedcontent_set.all():
            if relatedcontent_dict.has_key(relatedcontent.object._meta.module_name):
                object_list = relatedcontent_dict[relatedcontent.object._meta.module_name]
                object_list.extend(relatedcontent.object)
                relatedcontent_dict[relatedcontent.object._meta.module_name] = object_list
            else:
                relatedcontent_dict[relatedcontent.object._meta.module_name] = [relatedcontent.object]
        return relatedcontent_dict

    def get_geotags(self):
#        import ipdb; ipdb.set_trace()
        geo_dict = {}
        geo_dict['point'] = Point.objects.filter(content_type=ContentType.objects.get_for_model(self.__class__()), object_id=self.id)
        geo_dict['line'] = Line.objects.filter(content_type=ContentType.objects.get_for_model(self.__class__()), object_id=self.id)
        geo_dict['multiline'] = MultiLine.objects.filter(content_type=ContentType.objects.get_for_model(self.__class__()), object_id=self.id)
        geo_dict['polygon'] = Polygon.objects.filter(content_type=ContentType.objects.get_for_model(self.__class__()), object_id=self.id)
        return geo_dict

    def is_published(self):
        if self.status == STORY_STATUS_PUBLISHED:
            return True
        return False

    def is_draft(self):
        if self.status == STORY_STATUS_DRAFT:
            return True
        return False
    
class RelatedContent(models.Model):
    """
    RelatedContent allow you link any django object to
    a story
    """
    story = models.ForeignKey(Story)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey()
    
    class Meta:
        verbose_name = _("related content")
        verbose_name_plural = _("related contents")

    def __unicode__(self):
        return u"%s" % self.object

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
    A Page within a Story
    """
    story = models.ForeignKey(Story)
    content = models.TextField()
    tags = SuperTagField()
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
        
    @property
    def url(self):
        return "%s?p=%d" % (self.story.get_absolute_url(),self.pagenum,)
        
    @property
    def columns(self):
        """
        Split the page's content into columns based on HTML comments containing
        "Column Break".
        
        The split is done with regex so it is forgiving of the formatting. Examples:
            <!--columnbreak-->
            <!--   COLUMN   BREAK   -->
            <!-- Column Break -->
            <!-- ColumnBreak -->
        """
        colbrk = re.compile(r'<!--\s*column\s*break\s*-->',re.IGNORECASE)
        cols = re.split(colbrk,self.content)
        return cols
    
    @property
    def media(self):
        return self.detect_media()
    
    def detect_media(self):
        #TODO: strip out inserts that aren't the story media list
        template = Template("{%% load media_tags %%}%s" %  self.content)
        return [ Media.objects.get(pk=node.media_id.resolve(Context())).get_child_object() for node in template.nodelist if isinstance(node,MediaNode) ]
    
def reorder_story_pages(sender,**kwargs):
    story = kwargs['instance'].story
    Page.objects.update_page_order(story)
    
post_delete.connect(reorder_story_pages,Page)

