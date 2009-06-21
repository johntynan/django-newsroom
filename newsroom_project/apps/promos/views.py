from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from promos.forms import ImageForm
from promos.forms import LinkForm
from promos.forms import PromoForm
from promos.forms import DateForm
from promos.models import Promo
from promos.models import PromoImage
from promos.models import PromoLink
from promos.models import PromoDate
from utils.helpers import user_objects_qs


if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
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
            return HttpResponseRedirect(reverse('promos_image_list'))

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
            return HttpResponseRedirect(reverse('promos_promo_link_list'))

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
            return HttpResponseRedirect(reverse('promos_promo_date_list'))

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
                reverse('promos_promo_detail', args=[promo.id]))
    form = form_class(instance=geotag)

    context = RequestContext(request, {
        "form": form,
        "geo_type": form_class._meta.model._meta.verbose_name,
        "promo": promo,
        "google_key": settings.GOOGLE_MAPS_API_KEY,
        "geotag": geotag,
    })
    return render_to_response(template, context_instance=context )

