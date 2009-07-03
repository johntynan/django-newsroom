from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from flash.forms import FlashProjectForm, PosterFrameForm
from flash.models import FlashProject
from stories.models import RelatedContent

#TODO: add authentication check decorators

def flashproject_add_edit(request, media_id=None, template='flash/flashproject_add_edit.html', redirect_to='multimedia_browse', context_dict={}, story=None):

    fp = None
    if media_id:
        fp = get_object_or_404(FlashProject,pk=media_id)

    if request.method == 'POST':
        if fp:
            form = FlashProjectForm(request.POST,request.FILES, instance=fp)
            frame_form = PosterFrameForm(
                            request.POST, request.FILES,instance=fp.poster_frame)
        else:
            form = FlashProjectForm(request.POST,request.FILES)
            frame_form = PosterFrameForm(request.POST, request.FILES)
            
        if form.is_valid() and frame_form.is_valid():
            fp = form.save(commit=False)
            fp.modified_by = request.user
            fp.slug = slugify(fp.title)
            if not media_id:
                fp.site = Site.objects.get_current()
                fp.created_by = request.user
            frame = frame_form.save()
            old_frame = None
            if frame != fp.poster_frame:
                old_frame = fp.poster_frame
                fp.poster_frame = frame

            fp.save()
            form.save_m2m()
            if story:
                RelatedContent(story=story, object=fp).save()
                if story.sites.count() > 0:
                    fp.sites = story.sites.all()
                    fp.save()

            if old_frame:
                old_frame.image.delete()
                old_frame.delete()

            request.user.message_set.create(
                        message='Your flash project was saved.')
            return HttpResponseRedirect(reverse(redirect_to))
    else:
        if fp:
            form = FlashProjectForm(instance=fp)
            frame_form = PosterFrameForm(instance=fp.frame)
        else:
            form = FlashProjectForm()
            frame_form = PosterFrameForm()
            
    c = {'object': fp, 'form':form, 'frame_form':frame_form}
    context_dict.update(c)

    return render_to_response( 
                template, 
                context_dict,
                context_instance=RequestContext(request))


def flashproject_detail(request, fp_id,slug):
    fp = get_object_or_404(Video,pk=fp_id)
    return render_to_response(
                'flash/flashproject_detail.html',
                {'object':fp,},
                context_instance=RequestContext(request))

