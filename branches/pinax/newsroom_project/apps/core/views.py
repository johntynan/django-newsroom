# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 ai:
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.localflavor.us.models import USStateField
from django.template import Template, Context
from django.contrib.sites.models import Site

from core.models import Affiliate

from countries.models import Country
from core.constants import COMMENT_STATUS_CHOICES, COMMENT_STATUS_OPEN

def affiliate_list(request):
    affiliate_list = Affiliate.objects.all()
    return render_to_response(
            'affiliates/affiliate_list.html',
            {'affiliate_list': affiliate_list},              
            context_instance=RequestContext(request))

def affiliate_detail(request, id):
    """
    Get affiliate details.
    """
    affiliate = Affiliate.objects.get(pk=id)

    return render_to_response(
              'affiliates/affiliate_detail.html',{
              'affiliate': affiliate
              },
              context_instance=RequestContext(request))

def affiliate_add(request):
    """
    Process a new affiliate submission.
    """

    if request.method == "POST":
        form = AffiliateForm(request.POST)
        if form.is_valid():
            affiliate = form.save(commit=False)
            affiliate.submitter = request.user
            affiliate.save()
            request.user.message_set.create(
                message='Your affiliate has been submitted.')
            return HttpResponseRedirect(reverse('affiliates_affiliate_list'))

    else:
        form = AFfiliateForm()

    return render_to_response(
              'affiliates/affiliate_add.html',
              {'form':form},
              context_instance=RequestContext(request))

def affiliate_edit(request, id):
    """
    Edit an existing affiliate.
    """
    affiliate = get_object_or_404(Affiliate, pk=id)
    
    if request.method == "POST":
        form = AffiliateForm(request.POST, instance=affiliate)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your affiliate has been edited.')
            return HttpResponseRedirect(reverse('affiliates_affiliate_list'))
    else:
        form = AffiliateForm(instance=affiliate)        

    return render_to_response(
              'affiliates/affiliate_edit.html',
              {'form':form},
              context_instance=RequestContext(request))
