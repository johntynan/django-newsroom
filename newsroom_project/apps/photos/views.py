from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from photos.forms import PhotoForm, ImageForm
from photos.models import Photo

def photo_add_edit( request, media_id=None, template='photos/photo_add_edit.html', redirect_to='multimedia_browse', context_dict={}, story=None):

    if media_id:
        photo = get_object_or_404(Photo,pk=media_id)
    else:
        photo = None

    if request.method == 'POST':

        # Create edit or add form
        if photo:
            form = PhotoForm(request.POST,request.FILES, instance=photo)
            image_form = ImageForm(
                            request.POST, request.FILES,instance=photo.image)
        else:
            form = PhotoForm(request.POST,request.FILES)
            image_form = ImageForm( request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            photo = form.save(commit=False)
            image = image_form.save(commit=False)
            photo.modified_by = request.user
            photo.slug = slugify(photo.title)
            image.modified_by = request.user
            
            if not media_id:
                photo.site = Site.objects.get_current()
                photo.created_by = request.user
                image.created_by = request.user

            image.save()
            photo.image = image
            photo.save()

            image_form.save_m2m()
            form.save_m2m()

            if story:
                story.media.add(photo)

            request.user.message_set.create(
                        message='Your photo was saved.')            
            return HttpResponseRedirect(reverse(redirect_to))

    else:
        if photo:
            form = PhotoForm(instance=photo)
            image_form = ImageForm(instance=photo.image)
        else:
            form = PhotoForm()
            image_form = ImageForm()
            
    c = {'object':photo, 'form':form, 'image_form':image_form,}
    context_dict.update(c)

    return render_to_response(
                template,
                context_dict,
                context_instance=RequestContext(request))

