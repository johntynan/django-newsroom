from django.template import RequestContext
from django.shortcuts import render_to_response
#from photologue.models import Photo
from utils.response import JsonResponse, JsonErrorResponse
from multimedia.models import Video, Image

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
    
    
    
    
