from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from flash.models import Flash, FlashArchive
from flash.forms import FlashForm, FlashArchiveForm

@login_required
def flash_list(request):
    """
    Get index of flash files.
    """

    flash_list = Flash.objects.all()
    return render_to_response(
            'flash/flash_list.html',
            {'flash_list': flash_list},              
            context_instance=RequestContext(request))
    
@login_required
def flash_detail(request, id):
    flash_detail = Flash.objects.get(id=id)

    return render_to_response(
            'flash/flash_detail.html',{
                'flash_detail': flash_detail
             }, context_instance=RequestContext(request))

