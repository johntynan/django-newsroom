from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from django.db import models
from django.contrib.localflavor.us.models import USStateField
from django.template import Template, Context
from django.contrib.sites.models import Site
from countries.models import Country

from core.models import Affiliate

class AffiliateForm(forms.ModelForm):

    class Meta:
        model = Affiliate

