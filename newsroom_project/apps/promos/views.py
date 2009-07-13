from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from promos.forms import *
from promos.models import *
from utils.helpers import user_objects_qs
from notification import models as notification


from django.core.mail import send_mail

@login_required
def front(request):
    return render_to_response(
              'promos/front.html',
              {},
              context_instance=RequestContext(request))

@login_required
def promo_add(request):
    """
    Process a new promo submission.
    """

    if request.method == "POST":
        form = PromoForm(request.POST)
        if form.is_valid():
            promo = form.save(commit=False)
            promo.submitter = request.user
            promo.save()
#            promo.authors = form.cleaned_data["authors"]
#            promo.save()
            form.save_m2m()
            to_user = [mail_tuple[1] for mail_tuple in settings.PROMO_MODERATORS]
            message = render_to_string('promos/promo_sent.txt', { 'user': request.user , 'current_site': Site.objects.get_current().domain, 'object': promo.id })
            send_mail("promo_submitted", message, settings.DEFAULT_FROM_EMAIL, to_user)
            request.user.message_set.create(
                message='Your promo has been submitted.')

            return HttpResponseRedirect(reverse('promos_promo_list'))

    else:
        form = PromoForm()

    return render_to_response(
              'promos/promo_add.html',
              {'form':form},
              context_instance=RequestContext(request))

@login_required
def promo_edit(request, promo_id):
    """
    Edit an existing promo.
    """
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)

    if request.method == "POST":
        form = PromoForm(request.POST, instance=promo)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your promo has been edited.')
            return HttpResponseRedirect(reverse('promos_promo_list'))
    else:
        form = PromoForm(instance=promo)        

    return render_to_response(
              'promos/promo_edit.html',
              ({'form': form,
              'promo':promo}),
              context_instance=RequestContext(request))

@login_required
def promo_list(request):
    """
    Get index of promos.
    """

    user_promos = user_objects_qs(Promo, request.user)
    promo_image = PromoImage.objects.all()

    return render_to_response(
                'promos/promo_list.html',{
                'promos': user_promos,
                'promo_image': promo_image,
                },
              context_instance=RequestContext(request))
            
@login_required
def promo_detail(request, promo_id):
    """
    Get promo details.
    """
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)
    # do not use this: promo_link = promo.promolink_set.all() - a pain for introspection.
    promo_link = PromoLink.objects.filter(promo=promo_id)
    promo_image = PromoImage.objects.filter(promo=promo_id)

    return render_to_response(
            'promos/promo_detail.html',{
            'promo': promo,
            'promo_link': promo_link,
            'promo_image': promo_image,
            'google_key': settings.GOOGLE_MAPS_API_KEY,
             },
              context_instance=RequestContext(request))

@login_required
def promo_image_list(request, promo_id):
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)
    promo_image = PromoImage.objects.filter(promo=promo_id)
    return render_to_response(
            'promos/promo_image_list.html',{
            'promo':promo,
            'promo_image':promo_image,
            },
            context_instance=RequestContext(request))

@login_required
def promo_link_list(request, promo_id):
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)
    promo_link = PromoLink.objects.filter(promo=promo_id)
    return render_to_response(
            'promos/promo_link_list.html',{
            'promo':promo,
            'promo_link':promo_link,
            },
            context_instance=RequestContext(request))

@login_required
def promo_image_add(request, promo_id):
    """
    Process a new promo link submission.
    """
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            promo_image = form.save(commit=False)
            promo_image.promo = promo
            promo_image.save()
            request.user.message_set.create(
                message='Your promo image has been added.  Thank you.')
            return HttpResponseRedirect(reverse('promos_promo_image_list', args=[promo.id]))

    else:
        form = ImageForm()

    return render_to_response(
              'promos/promo_image_add.html',
              {'form':form,
              'promo':promo},
              context_instance=RequestContext(request))

@login_required
def promo_link_add(request, promo_id):
    """
    Process a new promo link submission.
    """
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            promo_link = form.save(commit=False)
            promo_link.promo = promo
            promo_link.save()

            request.user.message_set.create(
                message='Your promo link has been added.  Thank you.')
            return HttpResponseRedirect(
                reverse('promos_promo_link_list', args=[promo.id]))

    else:
        form = LinkForm()

    return render_to_response(
              'promos/promo_link_add.html',
              {'form':form,
              'promo':promo},
              context_instance=RequestContext(request))

@login_required
def promo_date_list(request, promo_id):
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)
    promo_date = PromoDate.objects.filter(promo=promo_id)
    return render_to_response(
            'promos/promo_date_list.html',{
            'promo':promo,
            'promo_date':promo_date,
            },
            context_instance=RequestContext(request))

@login_required
def promo_date_add(request, promo_id):
    """
    Process a new promo date submission.
    """
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)
    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            promo_date = form.save(commit=False)
            promo_date.promo = promo
            promo_date.save()
            
            request.user.message_set.create(
                message='Your promo date has been added.  Thank you.')
            return HttpResponseRedirect(reverse('promos_promo_date_list', args=[promo.id]))

    else:
        form = DateForm()

    return render_to_response(
              'promos/promo_date_add.html',
              {'form':form,
              'promo':promo},
              context_instance=RequestContext(request))

@login_required
def promo_add_edit_geotag(request,promo_id,
    template=None, form_class=None, geotag_class=None):
    """
    This view determines the content_type and the
    object_id for the given promo (promo_id) then it returns
    the response of add_edit_geotag.
    """
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)
    promo_content_type = ContentType.objects.get_for_model(promo)
    try:
        geotag = geotag_class.objects.get(content_type__pk=promo_content_type.id,
                               object_id=promo.id)
    except ObjectDoesNotExist:
        geotag = None
    if request.method == "POST":
        form = form_class(request.POST, instance=geotag)
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.object = promo
            new_object.save()
            return HttpResponseRedirect(
                reverse('promos_promo_add_edit_point', args=[promo.id]))
    form = form_class(instance=geotag)

    context = RequestContext(request, {
        "form": form,
        "geo_type": form_class._meta.model._meta.verbose_name,
        "promo": promo,
        "google_key": settings.GOOGLE_MAPS_API_KEY,
        "geotag": geotag,
    })
    return render_to_response(template, context_instance=context )

@login_required
def promo_billboard_list(request, promo_id):
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)
    promo_billboard = PromoBillboard.objects.filter(promo=promo_id)
    return render_to_response(
            'promos/promo_billboard_list.html',{
            'promo':promo,
            'promo_billboard':promo_billboard,
            },
            context_instance=RequestContext(request))

@login_required
def promo_billboard_add(request, promo_id):
    """
    Process a new promo billboard submission.
    """
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)
    if promo.promoimage_set.count() == 0:
        return render_to_response(
              'promos/promo_billboard_add_no_image.html',
              {'promo':promo},
              context_instance=RequestContext(request))
    if request.method == "POST":
        form = BillboardForm(request.POST)
        if form.is_valid():
            promo_billboard = form.save(commit=False)
            promo_billboard.promo = promo
            promo_billboard.save()
            form.save_m2m()

            request.user.message_set.create(
                message='Your promo billboard has been added.  Thank you.')
            to_user = [mail_tuple[1] for mail_tuple in settings.PROMO_MODERATORS]
            message = render_to_string('promos/billboard_sent.txt',
                                       { 'user': request.user ,
                                        'current_site': Site.objects.get_current().domain,
                                        'promo': promo,
                                        'billboard':promo_billboard})
            send_mail("billboard_submitted", message, settings.DEFAULT_FROM_EMAIL, to_user)
            return HttpResponseRedirect(
                reverse('promos_promo_billboard_list', args=[promo.id]))

    else:
        form = BillboardForm()
        form.fields["image"].queryset = promo.promoimage_set.filter(
            image_kind="B")

    return render_to_response(
              'promos/promo_billboard_add.html',
              {'form':form,
              'promo':promo},
              context_instance=RequestContext(request))

@login_required
def promo_billboard_detail(request, promo_id, billboard_id):
    """
    Get promo details.
    """
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)

    user_billboards = user_objects_qs(PromoBillboard, request.user)
    billboard = get_object_or_404(user_billboards, pk=billboard_id)
    if promo != billboard.promo:
        raise Http404()  

    return render_to_response(
            'promos/promo_billboard_detail.html',{
            'promo': promo,
            'billboard': billboard,

             },
              context_instance=RequestContext(request))

def promo_preview(request, promo_id):
    """
    Get promo details.
    """
    promo = Promo.objects.get(id=promo_id)
    promo_link = PromoLink.objects.filter(promo=promo_id)
    promo_image = PromoImage.objects.filter(promo=promo_id)
    promo_date = PromoDate.objects.filter(promo=promo_id)
    promo_billboard = PromoBillboard.objects.filter(promo=promo_id)

    return render_to_response(
            'promos/preview01.html',{
            'promo': promo,
            'promo_link': promo_link,
            'promo_image': promo_image,
            'promo_date': promo_date,
            'promo_billboard': promo_billboard,
            'google_key': settings.GOOGLE_MAPS_API_KEY,
             },
              context_instance=RequestContext(request))

@login_required
def promo_link_edit(request, promo_id, link_id):
    """
    Edit promo link.
    """
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)
    promo_link = PromoLink.objects.filter(promo=promo_id)

    if request.method == "POST":
        form = LinkForm(request.POST, instance=promo_link)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your promo link has been edited.')
            return HttpResponseRedirect(reverse('promos_promo_link_list'))
    else:
        form = LinkForm(instance=promo_link)        

    return render_to_response(
              'promos/promo_link_edit.html',
              ({'form': form,
              'promo':promo,
              'promo_link':promo_link}),
              context_instance=RequestContext(request))

@login_required
def promo_image_edit(request, promo_id, image_id):
    """
    Edit promo image.
    """
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)
    promo_image = PromoImage.objects.filter(promo=promo_id)

    if request.method == "POST":
        form = ImageForm(request.POST, instance=promo_image)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your promo image has been edited.')
            return HttpResponseRedirect(reverse('promos_promo_image_list'))
    else:
        form = LinkForm(instance=promo_image)        

    return render_to_response(
              'promos/promo_image_edit.html',
              ({'form': form,
              'promo':promo,
              'promo_image':promo_image}),
              context_instance=RequestContext(request))

@login_required
def promo_date_edit(request, promo_id, date_id):
    """
    Edit promo date.
    """
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)
    promo_date = PromoDate.objects.filter(promo=promo_id)

    if request.method == "POST":
        form = DateForm(request.POST, instance=promo_date)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your promo date has been edited.')
            return HttpResponseRedirect(reverse('promos_promo_date_list'))
    else:
        form = DateForm(instance=promo_link)

    return render_to_response(
              'promos/promo_date_edit.html',
              ({'form': form,
              'promo':promo,
              'promo_date':promo_date}),
              context_instance=RequestContext(request))

@login_required
def promo_billboard_edit(request, promo_id, billboard_id):
    """
    Edit promo billboard.
    """
    user_promos = user_objects_qs(Promo, request.user)
    promo = get_object_or_404(user_promos, pk=promo_id)
    promo_billboard = PromoBillboard.objects.get(id=billboard_id)

    if request.method == "POST":
        form = BillboardForm(request.POST, instance=promo_billboard)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your promo billboard has been edited.')
            return HttpResponseRedirect(
                reverse('promos_promo_billboard_list',
                        args=[promo.id]))
    else:
        form = BillboardForm(instance=promo_billboard)        

    return render_to_response(
              'promos/promo_billboard_edit.html',
              ({'form': form,
              'promo':promo,
              'promo_link':promo_billboard}),
              context_instance=RequestContext(request))

