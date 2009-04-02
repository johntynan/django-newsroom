# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 ai:
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse
from django.conf import settings
from my_profiles.forms import RegistrationForm, PasswordResetForm
from registration import views as reg_views
from profiles import views as prof_views
import datetime, random, sha

#from profiles import utils
#Profile = utils.get_profile_model()

def create_profile(request, **kwargs):
    return prof_views.create_profile(request, **kwargs)

def edit_profile(request, **kwargs):
    return prof_views.edit_profile(request, **kwargs)

def profile_detail(request, username, **kwargs):
    return prof_views.profile_detail(request, username, **kwargs)

def profile_list(request, **kwargs):
    return prof_views.profile_list(request, **kwargs)

def register(request, form_class=RegistrationForm):

    if request.user.is_authenticated():
        # They are logged in, redirect to user account page
        return HttpResponseRedirect( reverse('profiles_create_profile'))

    return reg_views.register(request, form_class=form_class)


def activate(request, activation_key, **kwargs):

    if request.user.is_authenticated():
        request.user.message_set.create(message="You are already logged in.")
        return HttpResponseRedirect(reverse('profiles_create_profile'))

    return reg_views.activate(request, activation_key, **kwargs)


def password_reset(request, password_reset_form=PasswordResetForm):
    return auth_views.password_reset(
            request, password_reset_form=password_reset_form)

