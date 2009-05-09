from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.defaultfilters import slugify
from photos.forms import PhotoForm, PhotoImageForm
from photos.models import Photo

def photo_edit(request, photo_id):
    photo = get_object_or_404(Photo,pk=photo_id)

    if request.method == 'POST':
        form = PhotoForm(request.POST,request.FILES, instance=photo)
        # don't include instance, only process the POST/FILES data
        # for the image form
        image_form = PhotoImageForm(
                        request.POST, request.FILES,instance=photo.image)
        if form.is_valid() and image_form.is_valid():
            photo = form.save(commit=False)
            photo.modified_by = request.user
            photo.slug = slugify(photo.title)
            image = image_form.save()
            old_image = None
            if image != photo.image:
                old_image = photo.image
                photo.image = image

            photo.save()
            form.save_m2m()

            if old_image:
                print 'try deleting old image'
                old_image.image.delete()
                old_image.delete()

            request.user.message_set.create(
                        message='Your photo was saved.')            
            return HttpResponseRedirect(reverse('multimedia_browse'))
    else:
        form = VideoForm(instance=photo)
        image_form = VideoFrameForm(instance=photo.image)

    return render_to_response('photos/photo_edit.html',locals(),context_instance=RequestContext(request))

