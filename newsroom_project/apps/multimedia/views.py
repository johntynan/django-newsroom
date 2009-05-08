from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.shortcuts import render_to_response, get_object_or_404

from multimedia.forms import MediaForm
from multimedia.models import Media#, Video, Image
from utils.response import JsonResponse, JsonErrorResponse

@login_required    
def detail(request,media_id,slug=None):

    object = get_object_or_404(Media, pk=media_id)

    return render_to_response('multimedia/media_detail.html',locals(),context_instance=RequestContext(request))

def preview(request,media_id):

    object = get_object_or_404(Media, pk=media_id)

    return render_to_response('multimedia/media_preview.html',locals(),context_instance=RequestContext(request))

@login_required    
def browse(request):

    media_items = request.user.media_set.all()

    return render_to_response('multimedia/browse_media.html',locals(),context_instance=RequestContext(request))

@login_required    
def browse_by_type(request,media_type):
    
    try:
        media_class = Media.class_factory(media_type)
    except KeyError:
        # TODO raise an exception more specific than KeyError?
        raise Http404('Media type not supported.')
    #media_items = media_class.on_site.all()
    media_items = media_class.objects.filter(authors__in=[request.user])
    
    print type(media_items[0])
    print media_items[0].get_thumbnail_url()
    #if request.is_ajax():
        
    #    return JsonResponse()
    return render_to_response('multimedia/browse_media.html',locals(),context_instance=RequestContext(request))
    

@login_required    
def add_by_type(request,media_type):
    
    try:
        form_class = MediaForm.factory(media_type)
    except KeyError:
        # TODO raise an exception more specific than KeyError?
        raise Http404('Media type not supported.')
        
    if request.method == 'POST':
        form = form_class(request.POST,request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.created_by = request.user
            media.modified_by = request.user
            media.slug = slugify(media.title)
            media.site = Site.objects.get_current()
            media.save()
            form.save_m2m()
            request.user.message_set.create(
                        message='Your media was saved.')
            return HttpResponseRedirect(
                        reverse(browse))
    else:
        form = form_class()
    
    return render_to_response('multimedia/add_media.html',locals(),context_instance=RequestContext(request))
    
    

@login_required    
def edit(request, media_id):
    
    media = get_object_or_404(Media, pk=media_id)
    object = media.get_child_object()

    try:
        form_class = MediaForm.factory(object.media_type)
    except KeyError:
        # TODO raise an exception more specific than KeyError?
        raise Http404('Media type not supported.')

    if request.method == 'POST':
        form = form_class(request.POST,request.FILES, instance=object)
        if form.is_valid():
            media = form.save(commit=False)
            media.modified_by = request.user
            media.slug = slugify(media.title)
            media.save()
            form.save_m2m()
            request.user.message_set.create(
                        message='Your media was saved.')
            return HttpResponseRedirect(
                        reverse(browse))
    else:
        form = form_class(instance=object)

    return render_to_response('multimedia/edit_media.html',locals(),context_instance=RequestContext(request))
    
