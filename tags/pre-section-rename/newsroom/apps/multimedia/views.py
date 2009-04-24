from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
#from photologue.models import Photo
from utils.response import JsonResponse, JsonErrorResponse
from multimedia.forms import MediaForm
from multimedia.models import Media, Video, Image

def browse_by_type(request,media_type):
    #TODO use introspection to make DRY
    if "image" == media_type:
        media_items = Image.objects.all()
    elif "video" == media_type:
        #TODO filter by author/owner
        media_items = Video.objects.all()
    
    #if request.is_ajax():
        
    #    return JsonResponse()
    return render_to_response('multimedia/browse_media.html',locals(),context_instance=RequestContext(request))
    
    
def add_by_type(request,media_type):
    
    if request.method == 'POST':
        pass
    else:
        #if not media_type in Media.media_types:
        #    return Http404
        #if "video" == media_type:
        #    return HttpResponseRedirect(reverse('videos_add_video'))
        #elif "image" == media_type:
        #    pass
        form = MediaForm()
        return render_to_response('multimedia/add_media.html',locals(),context_instance=RequestContext(request))
    
    
    
