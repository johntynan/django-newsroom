from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from videos.forms import VideoForm
from videos.models import Video

#TODO: add authentication check decorators

def add_video(request):
    """
    Create a new Video for the user
    """
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.created_by = request.user
            video.modified_by = request.user
            video.save()
            return HttpResponseRedirect(reverse('videos_video_detail',args=[video.id]))
    else:
        form = VideoForm()

    return render_to_response(
                'videos/video_add.html',
                locals(),
                context_instance=RequestContext(request))

def video_detail(request,video_id):
    video = get_object_or_404(Video,pk=video_id)
    return render_to_response(
                'videos/video_detail.html',
                locals(),
                context_instance=RequestContext(request))



