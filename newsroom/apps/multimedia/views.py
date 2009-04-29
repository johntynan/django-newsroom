from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.shortcuts import render_to_response

from multimedia.forms import MediaForm
from multimedia.models import Media#, Video, Image
from utils.response import JsonResponse, JsonErrorResponse

#TODO: login req?
def browse_by_type(request,media_type):
    
    media_class = Media.class_factory(media_type)
    #media_items = media_class.on_site.all()
    media_items = media_class.children.all()
    
    print type(media_items[0])
    print media_items[0].get_thumbnail_url()
    #if request.is_ajax():
        
    #    return JsonResponse()
    return render_to_response('multimedia/browse_media.html',locals(),context_instance=RequestContext(request))
    

@login_required    
def add_by_type(request,media_type):
    
    form_class = MediaForm.factory(media_type)
    if request.method == 'POST':
        form = form_class(request.POST,request.FILES)
        media = form.save(commit=False)
        media.created_by = request.user
        media.modified_by = request.user
        media.slug = slugify(media.title)
        media.site = Site.objects.get_current()
        media.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse(browse_by_type,args=[media_type,]))
    else:
        form = form_class()
    
    return render_to_response('multimedia/add_media.html',locals(),context_instance=RequestContext(request))
    
    
    
