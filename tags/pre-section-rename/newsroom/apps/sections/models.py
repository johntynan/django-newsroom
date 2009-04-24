from django.db import models
from stories.models import Story

class SectionPath(models.Model):
    """
    A Section Path is a term we are using to describe free-from strings defined by editors or authors that allow you to categorize content.
    The strings follow a simple convention using forward slashes:

    /people/george_bush
    /places/europe/france/region/paris/neighborhood
    /topics/immigration
    /events/2009/inauguration
    /topics/housing

    """
    section_path = models.CharField(max_length=256)

    def __unicode__(self):
        return self.section_path
        

class Section(models.Model):
    """
    Sections are a top level collection of stories grouped by topic.
    For instance, a section on the site related to the Housing Crisis could list stories based on the following more general topics:
    "housing," "banking," "mortgages"
    and would live under the site at http://news21.com/economy/housing-crisis/
    the section_path would be responsible for gathering the section paths for housing, banking and mortages
    and the section_slug would be responsible for creating the url economy/housing-crisis from the root of the site.
    The section Title would be a string, like "The Home Mortage Meltdown"
    There might also be a section description.
    """
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    collection = models.ManyToManyField(SectionPath) 
        
    def __unicode__(self):
        return self.title
