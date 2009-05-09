from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.defaultfilters import slugify
from videos.forms import VideoForm, VideoFrameForm
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
            video.slug = slugify(video.title)
            video.save()
            # we need to save authors in extra step because they are manytomany
            form.save_m2m()
            request.user.message_set.create(
                    message='Your video has been saved.')
            return HttpResponseRedirect(reverse('videos_video_detail',args=[video.id]))
    else:
        form = VideoForm()

    return render_to_response(
                'videos/video_add.html',
                locals(),
                context_instance=RequestContext(request))

def video_edit(request, video_id):

    video = get_object_or_404(Video,pk=video_id)

    if request.method == 'POST':
        form = VideoForm(request.POST,request.FILES, instance=video)
        # don't include instance, only process the POST/FILES data
        # for the frame form
        frame_form = VideoFrameForm(
                        request.POST, request.FILES,instance=video.frame)
        if form.is_valid() and frame_form.is_valid():
            video = form.save(commit=False)
            video.modified_by = request.user
            video.slug = slugify(video.title)
            frame = frame_form.save()
            old_frame = None
            if frame != video.frame:
                old_frame = video.frame
                video.frame = frame

            video.save()
            form.save_m2m()

            if old_frame:
                print 'try deleting old frame'
                old_frame.image.delete()
                old_frame.delete()

            request.user.message_set.create(
                        message='Your video was saved.')            
            return HttpResponseRedirect(reverse('multimedia_browse'))
    else:
        form = VideoForm(instance=video)
        frame_form = VideoFrameForm(instance=video.frame)

    return render_to_response('videos/video_edit.html',locals(),context_instance=RequestContext(request))


def video_detail(request,video_id,slug):
    video = get_object_or_404(Video,pk=video_id)
    return render_to_response(
                'videos/video_detail.html',
                {'object':video,},
                context_instance=RequestContext(request))



