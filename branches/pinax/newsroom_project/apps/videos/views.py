from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
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

def video_add_edit(request, media_id=None, template='videos/video_add_edit.html', redirect_to='multimedia_browse', context_dict={}, story=None):

    video = None
    if media_id:
        video = get_object_or_404(Video,pk=media_id)

    if request.method == 'POST':
        if video:
            form = VideoForm(request.POST,request.FILES, instance=video)
            frame_form = VideoFrameForm(
                            request.POST, request.FILES,instance=video.frame)
        else:
            form = VideoForm(request.POST,request.FILES)
            frame_form = VideoFrameForm(request.POST, request.FILES)
            
        if form.is_valid() and frame_form.is_valid():
            video = form.save(commit=False)
            video.modified_by = request.user
            video.slug = slugify(video.title)
            if not media_id:
                video.site = Site.objects.get_current()
                video.created_by = request.user
            frame = frame_form.save()
            old_frame = None
            if frame != video.frame:
                old_frame = video.frame
                video.frame = frame

            video.save()
            form.save_m2m()
            if story:
                story.media.add(video)
                if story.sites.count() > 0:
                    video.sites = story.sites.all()
                    video.save()

            if old_frame:
                print 'deleting old frame'
                old_frame.image.delete()
                old_frame.delete()

            request.user.message_set.create(
                        message='Your video was saved.')
            return HttpResponseRedirect(reverse(redirect_to))
    else:
        if video:
            form = VideoForm(instance=video)
            frame_form = VideoFrameForm(instance=video.frame)
        else:
            form = VideoForm()
            frame_form = VideoFrameForm()
            
    c = {'object': video, 'form':form, 'frame_form':frame_form}
    context_dict.update(c)

    return render_to_response( 
                template, 
                context_dict,
                context_instance=RequestContext(request))


def video_detail(request,video_id,slug):
    video = get_object_or_404(Video,pk=video_id)
    return render_to_response(
                'videos/video_detail.html',
                {'object':video,},
                context_instance=RequestContext(request))



