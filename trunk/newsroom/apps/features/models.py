from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from core.models import Project
from photologue.models import Photo
from bookmarks.models import BookmarkInstance
from sections.models import SectionPath

class Feature(models.Model):
    """
    A feature is use to define what will appear on the front page of the site
    for some period of time.

    When affiliates want a story or project syndicated through this site
    they submit a feature.  This is where some data gets saved for the 
    editor to sift through later and contruct a home page.
    """

    headline =  models.CharField(max_length=255)
    permalink = models.URLField(
                    unique=True,
                    verify_exists=False,
                    help_text="This should be the published link for the story or project you want featured on news21.com. <br />e.g. http://features.csmonitor.com/globalnews/2009/03/30/ahead-of-north-koreas-planned-rocket-launch-us-dispatches-destroyers/")
    project = models.ManyToManyField(Project)
    submitter = models.ForeignKey(
                    User,
                    related_name='features_submitted',)
    authors = models.ManyToManyField(
                User,
                related_name='features_authored',
                help_text="The authors of the published work.")
    other_credits = models.TextField(
                      blank=True,
                      help_text="If the authors are not available in the list above please include their names here.",)

    relevance_begins = models.DateField(
                        "Suggested Relevance Begins",
                        help_text="Suggested date span for use on home page.")
    relevance_ends = models.DateField(
                        "Suggested Relevance Ends",)
    
    section = models.ManyToManyField(SectionPath)

    # last_featured is not editable and is managed by the front page
    # view code.
    last_featured = models.DateTimeField(
                        editable=False,
                        blank=True,
                        null=True)
    expires = models.DateTimeField(
                blank=True,
                null=True,)
    
    def __unicode__(self):
       return self.headline

    def get_absolute_url(self):
        return ('features_feature_detail', 
                (), 
                { 'id': self.id })
    get_absolute_url = models.permalink(get_absolute_url)


class FeatureLink(models.Model):
    """
    Links related to feature submissions.
    """
    title = models.CharField(max_length=200)
    url = models.URLField(verify_exists=False)
    desc = models.TextField('description',blank=True)
    feature = models.ForeignKey(
                Feature,
                help_text='Related links might be a blog post or other information related to how the piece was built, "behind the scenes", or just links related to the same topic.')

    def __unicode__(self):
        return self.title

class FeatureImage(models.Model):
    photo = models.ForeignKey(Photo)
    feature = models.ForeignKey(
                Feature,
                help_text="Photos to help with featuring the piece.  The photos ideally are 16:9 or 4:3 aspect ratio and 1000px wide.  Scaling and thumbnails are handled automatically.",)


    def __unicode__(self):
        return self.photo.title
