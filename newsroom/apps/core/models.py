
from django.contrib.auth.models import User
from django.db import models
from django.contrib.localflavor.us.models import USStateField
from countries.models import Country
from aggregator.models import Feed

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

#class Project(models.Model):
#    affiliate = models.ForeignKey(Affiliate)
#    url = models.URLField(
#            verify_exists=False,
#            help_text="The project's public web site.",)
