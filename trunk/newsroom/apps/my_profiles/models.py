from django.contrib.localflavor.us.models import PhoneNumberField, USStateField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals  
from imagekit.models import ImageModel
from core.models import Affiliate


IK_SPEC_MODULE = 'my_profiles.photo_specs'

class ProfileImage(ImageModel):
    """
    Define a profile image using an imagekit model.
    """
    image = models.ImageField(upload_to='uploads/my_profiles',)

    class IKOptions:
        spec_module = IK_SPEC_MODULE
        cache_dir = 'my_profiles'
        cache_filename_format = "%(specname)s/%(filename)s.%(extension)s"


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
    bio = models.TextField(blank=True)
    phone = PhoneNumberField(blank=True)
    twitter_name = models.CharField(
                    max_length=50,
                    blank=True,)
    location = models.CharField(
                blank=True,
                max_length=100,
                help_text="Your City, State or lat/lon.")

    mugshot = models.ForeignKey(
                ProfileImage, null=True, blank=True,
                help_text='A JPEG image of yourself or something that represents you.',)

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
