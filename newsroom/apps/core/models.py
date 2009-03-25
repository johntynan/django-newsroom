
from django.contrib.auth.models import User
from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField, USStateField
from countries.models import Country
from aggregator.models import Feed


class Person(models.Model):
    user = models.ForeignKey(User)
    affiliate = models.ForeignKey('Affiliate')
    middle_name = models.CharField(max_length="50")
    url = models.URLField(
            verify_exists=False,
            help_text="Your public web site.",)
    phone = PhoneNumberField(blank=True)
    twitter_name = models.CharField(max_length="50")
    location = models.CharField(
                blank=True,
                max_length="100",
                help_text="Your City and State or lat/lon.")
    
class Affiliate(models.Model):
    name = models.CharField(max_length="50")
    url = models.URLField(
            verify_exists=False,
            help_text="The affiliates's public web site.",)
    logo = models.ImageField(
            blank=True,
            upload_to="affiliates",)
    city = models.CharField(max_length="100")
    state = USStateField()
    country = models.ForeignKey(Country)

class AffiliateFeed(Feed):
    affiliate = models.ForeignKey(Affiliate)

class Project(models.Model):
    affiliate = models.ForeignKey(Affiliate)
    url = models.URLField(
            verify_exists=False,
            help_text="The project's public web site.",)
