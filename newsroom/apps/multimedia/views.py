from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from multimedia.forms import MediaForm
from multimedia.models import Media#, Video, Image
from utils.response import JsonResponse, JsonErrorResponse

def browse_by_type(request,media_type):
    
    media_class = Media.class_factory(media_type)
    media_items = media_class.objects.all()
    
    #if request.is_ajax():
        
    #    return JsonResponse()
    return render_to_response('multimedia/browse_media.html',locals(),context_instance=RequestContext(request))
    
    
def add_by_type(request,media_type):
    
    form_class = MediaForm.factory(media_type)
    if request.method == 'POST':
        form = form_class(request.POST)
    else:
        form = form_class()
        return render_to_response('multimedia/add_media.html',locals(),context_instance=RequestContext(request))
    
    
    
