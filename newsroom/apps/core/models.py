
from django.contrib.auth.models import User
from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField, USStateField
from django.db.models import signals  
from countries.models import Country
from aggregator.models import Feed
from core.signals import create_profile


class Person(models.Model):
    """
    Defines a person within the organization or as an Affiliate.

    Affiliate Foreign Key should be optional? TODO
    """
    user = models.ForeignKey(User, unique=True)
    affiliate = models.ForeignKey('Affiliate',null=True)
    middle_name = models.CharField(
                    max_length=50,
                    blank=True,)
    url = models.URLField(
            verify_exists=False,
            blank=True,
            help_text="Your public web site.",)
    phone = PhoneNumberField(blank=True)
    twitter_name = models.CharField(
                    max_length=50,
                    blank=True,)
    location = models.CharField(
                blank=True,
                max_length=100,
                help_text="Your City and State or lat/lon.")

    def __unicode__(self):
        if self.user.first_name:
            return "%s %s %s" % (self.user.first_name, 
                                 self.middle_name,
                                 self.user.last_name)
        return self.user.username

    def get_absolute_url(self):
        return ('profiles_profile_detail', 
                (), 
                { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)

signals.post_save.connect(create_profile, sender=User)
    
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
    affiliate = models.ForeignKey(Affiliate)
    url = models.URLField(
            verify_exists=False,
            help_text="The project's public web site.",)
