from django.contrib.localflavor.us.models import PhoneNumberField, USStateField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals  
from photologue.models import Photo
from core.models import Affiliate


class Profile(models.Model):
    """
    Defines extra information related to a person/user.
    Optionally adds a foreign key to an Affiliate.
    """
    user = models.OneToOneField(User, primary_key=True)  
    affiliate = models.ForeignKey(Affiliate,null=True)
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
                help_text="Your City, State or lat/lon.")

    mugshot = models.ForeignKey(Photo, null=True, blank=True)

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

    
def create_profile(sender, instance, signal, created, **kwargs):
    """When user is created also create a profile."""
    #from my_profiles.models import Profile
    if created:
        Profile(user = instance).save()

signals.post_save.connect(create_profile, sender=User)
