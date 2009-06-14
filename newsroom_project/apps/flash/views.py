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

from django.core.files.storage import FileSystemStorage

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

@login_required
def flash_add(request):
    """
    Process a new Flash object.
    """

    if request.method == "POST":
        form = FlashForm(request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your Flash object been added.  Thank you.')
            return HttpResponseRedirect(reverse('flash_flash_list'))

    else:
        #form = TopicForm(user=request.user)
        form = FlashForm()

    return render_to_response(
              'flash/flash_add.html',
              {'form':form},
              context_instance=RequestContext(request))
    
@login_required   
def flash_archive_add(request):
    """
    Upload a flash archive.
    """

    if request.method == "POST":
        form = FlashArchiveForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your flash archive has been added.  Thank you.')
            return HttpResponseRedirect(reverse('flash_flash_list'))

    else:
        form = FlashArchiveForm()

    return render_to_response(
              'flash/flash_archive_add.html',
              {'form':form},
              context_instance=RequestContext(request))