
from django.contrib.auth.models import User
from django.db import models
from django.contrib.localflavor.us.models import USStateField
from django.template import Template, Context
from countries.models import Country
from aggregator.models import Feed
from multimedia.models import Media

class Affiliate(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(
            verify_exists=False,
            help_text="The affiliates's public web site.",)
    logo = models.ImageField(
            blank=True,
            upload_to="affiliates",)
    city = models.CharField(max_length=100)
    state = USStateField()
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.name

class AffiliateFeed(Feed):
    affiliate = models.ForeignKey(Affiliate)

    def __unicode__(self):
        return "Feed for %s" % self.affiliate.name

class Project(models.Model):
    """
    A project is always related to an affiliate and relates to a page
    that defines a project's landing page.
    """

    affiliate = models.ManyToManyField(Affiliate)
    url = models.URLField(
            blank=True,
            verify_exists=False,
            help_text="Is the project a separate website? Provide the public URL if it has one.",)
    title = models.CharField(
                max_length=100,
                help_text='The title of the project. i.e. "The American Dream"')
    slug = models.SlugField(unique=True)
    summary = models.TextField(
                help_text='Provide a summary that can be used to describe the project.')

    activity_begins = models.DateField(
                        help_text="When does production begin for this project?")
    activity_ends = models.DateField(
                        help_text="When is all production forcasted to end for this project?")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('projects_project_detail', 
                (), 
                { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)


class PageManager(models.Manager):
    pass

class Page(models.Model):
    """
    A project landing page, similar to story pages but there are not 
    multiple pages.
    """
    project = models.ForeignKey(Project,unique=True)
    content = models.TextField(
                help_text='The landing page for the project.',)

    objects = PageManager()
    
        
    def __unicode__(self):
        return u"%s: Landing Page" % (self.project,)
    
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

