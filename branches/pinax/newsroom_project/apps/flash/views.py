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

import sys, zipfile, os, os.path


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

            handle_uploaded_file(request, request.FILES['file'], filename)
            
            request.user.message_set.create(message=message)
            return HttpResponseRedirect(reverse('flash_flash_list'))

    else:
        form = FlashArchiveForm()

    return render_to_response(
              'flash/flash_archive_add.html',
              {'form':form},
              context_instance=RequestContext(request))


def handle_uploaded_file(request, zip_file, filename):
    if zip_file.content_type != 'application/zip':
        message='File upload must be a valid ZIP archive.'
        request.user.message_set.create(message=message)
        return HttpResponseRedirect(reverse('flash_flash_list'))
    else:
        workingdir = settings.MEDIA_ROOT + '/flash/unzipped/' 
        foldername = filename.strip('.zip')
        fullpath = workingdir + foldername
        message = settings.MEDIA_ROOT + '/flash/unzipped/' 
        tempfile = open(fullpath+'.zip', 'wb+')
        
        for chunk in zip_file.chunks():
            tempfile.write(chunk)
                          
        zfile = zipfile.ZipFile(tempfile)
        os.mkdir(os.path.join(workingdir, foldername))

        for name in zfile.namelist():
            if name.endswith('/'):
                os.mkdir(os.path.join(workingdir, name))
            else:
                message = name
                newfile = os.path.join(workingdir, foldername, name)
                open(newfile, "wb")
                newfile.write(zfile.read(zfile.name()))
                # newfile.write(zfile.read(name))
                # newfile.write()
                newfile.close()

        tempfile.close()
        message = 'your file has been unzipped'

    
    request.user.message_set.create(message=message)
    return HttpResponseRedirect(reverse('flash_flash_list'))
