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

import zipfile

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
            message='Your flash archive has been added.  Thank you.'


            flash_archive = request.FILES
            filename = str(flash_archive['file'])

            handle_uploaded_file(request.FILES['file'], filename, message)
            
            request.user.message_set.create(message=message)
            return HttpResponseRedirect(reverse('flash_flash_list'))

    else:
        form = FlashArchiveForm()

    return render_to_response(
              'flash/flash_archive_add.html',
              {'form':form},
              context_instance=RequestContext(request))


def handle_uploaded_file(zip_file, filename, message):
    if zip_file.content_type != 'application/zip':
        message='File upload must be a valid ZIP archive.'
    else:
        try:
            fileandpath = settings.MEDIA_ROOT + '/flash/unzipped/' + filename
            destination = open(fileandpath, 'wb+')
            for chunk in zip_file.chunks():
                destination.write(chunk)
            destination.close()
            fileandpath

        except:
            message='could not unzip file'
    return zip_file, message # Return the zip_file